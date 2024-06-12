import json
from abc import ABC, abstractmethod


class Leaf:
    def __init__(self, name, icon=None, value=None):
        self.name = name
        self.icon = icon
        self.value = value

    def draw(self, level=0, prefix=''):
        name_part = f'{self.icon} {self.name}' if self.icon else f'{self.name}'
        if self.value is not None:
            name_part += f': {self.value}'
        return '  ' * level + prefix + name_part + '\n'


class Container:
    def __init__(self, name, icon=None):
        self.name = name
        self.icon = icon
        self.children = []

    def add(self, component):
        self.children.append(component)

    def draw(self, level=0, prefix=''):
        result = '  ' * level + prefix + (f'{self.icon} {self.name}\n' if self.icon else f'{self.name}\n')
        for i, child in enumerate(self.children):
            if i == len(self.children) - 1:
                result += child.draw(level + 1, '└─')
            else:
                result += child.draw(level + 1, '├─')
        return result


class AbstractFactory(ABC):
    @abstractmethod
    def create_leaf(self, name, value=None):
        pass

    @abstractmethod
    def create_container(self, name):
        pass


class PokerFaceFactory(AbstractFactory):
    def create_leaf(self, name, value=None):
        return Leaf(name, '♤', value)

    def create_container(self, name):
        return Container(name, '♢')


class DefaultFactory(AbstractFactory):
    def create_leaf(self, name, value=None):
        return Leaf(name, value=value)

    def create_container(self, name):
        return Container(name)


class JSONBuilder:
    def __init__(self, factory):
        self.factory = factory

    def build(self, data, name='root'):
        if isinstance(data, dict):
            container = self.factory.create_container(name)
            for key, value in data.items():
                container.add(self.build(value, key))
            return container
        elif isinstance(data, list):
            container = self.factory.create_container(name)
            for index, item in enumerate(data):
                container.add(self.build(item, f'item{index}'))
            return container
        else:
            return self.factory.create_leaf(name, data)


class RectangleDrawer:
    def draw(self, component):
        lines, _ = self._draw_rectangle(component)
        return "\n".join(lines)

    def _draw_rectangle(self, component, level=0, is_last=True):
        if isinstance(component, Leaf):
            prefix = '└─' if level == 0 else '├─' if not is_last else '└─'
            line = f'{prefix} {component.icon} {component.name}' if component.icon else f'{prefix} {component.name}'
            if component.value is not None:
                line += f': {component.value}'
            return [line], level

        prefix = '┌─' if level == 0 else '├─' if not is_last else '└─'
        line = f'{prefix} {component.icon} {component.name}' if component.icon else f'{prefix} {component.name}'
        lines = [line]
        for i, child in enumerate(component.children):
            child_lines, _ = self._draw_rectangle(child, level + 1, i == len(component.children) - 1)
            lines.extend([' ' * (2 * (level + 1)) + line for line in child_lines])
        return lines, level


class FunnyJsonExplorer:
    def __init__(self, factory):
        self.factory = factory

    def load(self, json_file):
        with open(json_file, 'r') as file:
            self.data = json.load(file)

    def show(self, style='tree'):
        builder = JSONBuilder(self.factory)
        structure = builder.build(self.data)
        if style == 'tree':
            return structure.draw()
        elif style == 'rectangle':
            drawer = RectangleDrawer()
            return drawer.draw(structure)
        else:
            raise ValueError("Unsupported style")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: fje -f <json file> -s <style> [-i <icon family>]")
        sys.exit(1)

    json_file = None
    style = None
    icon_family = None

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-f':
            json_file = sys.argv[i + 1]
        elif sys.argv[i] == '-s':
            style = sys.argv[i + 1]
        elif sys.argv[i] == '-i':
            icon_family = sys.argv[i + 1]

    if not json_file or not style:
        print("Usage: fje -f <json file> -s <style> [-i <icon family>]")
        sys.exit(1)

    if icon_family == 'poker-face-icon-family':
        factory = PokerFaceFactory()
    else:
        factory = DefaultFactory()

    explorer = FunnyJsonExplorer(factory)
    explorer.load(json_file)
    print(explorer.show(style=style))