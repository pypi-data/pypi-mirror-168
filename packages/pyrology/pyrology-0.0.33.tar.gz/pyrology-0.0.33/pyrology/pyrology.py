import importlib.machinery
import importlib.util
import os
from pathlib import Path



class Simplespace:
    def __getattr__(self, k):
        if k not in self.__dict__:
            self.__dict__[k] = Simplespace()
        return self.__dict__[k]
    def __getitem__(self, k):
        self.__getattr__(k)
        return self.__dict__[k]
    def __setattr__(self, k, v):
        self.__dict__[k] = v
    def __setitem__(self, k, v):
        self.__setattr__(k, v)



class Tablespace(Simplespace):
    def get(self, aPath):
        items = aPath.split('.')
        obj = self
        for item in items:
            obj = obj.__getitem__(item)
        return obj
    def set(self, aPath, aValue):
        items = aPath.split('.')
        obj = self
        for item in items[:-1]:
            obj = obj.__getitem__(item)
        obj.__setitem__(items[-1], aValue)
        return self
    def table(self, pop=False):
        def __flatten__(aSource, aDestination, name, pop):
            if (type(aSource) is dict):
                for key in aSource:
                    __flatten__(aSource[key], aDestination, name + key + '.', pop)
            elif (type(aSource) is list) and (pop):
                pos = 0
                for element in aSource:
                    __flatten__(element, aDestination, name + str(pos) + '.', pop)
                    pos += 1
            else:
                aDestination[name[:-1]] = aSource
            return aDestination
        return __flatten__(self.__toDictionary(), {}, '', pop)
    def __toDictionary(self):
        def __toDictionary__(aSource, aDestination):
            for key in aSource:
                value = aSource[key]
                if isinstance(value, Simplespace):
                    aDestination[key] = {}
                    __toDictionary__(value.__dict__, aDestination[key])
                else:
                    aDestination[key] = value
            return aDestination
        return __toDictionary__(self.__dict__, {})



class Dotspace(Tablespace):
    def load(self, aPath, aFile):
        self.__home(aPath)
        self.__read(f"{self.home}/{aFile}")
        return self
    def save(self, aPath):
        self.__home(aPath)
        return self
    def walk(self, aPath, aFilter=['*.py', '*.txt']):
        self.__home(aPath)
        paths = [list(Path(self.home).rglob(e)) for e in aFilter]
        for path in set().union(*paths):
            self.__read(str(path))
        return self
    def write(self, aPath, aFile):
        self.__home(aPath)
        return self
    def __home(self, aHome):
        if aHome[0] == '/':
            self.home = aHome
        else:
            self.home = f"{os.path.expanduser('~')}/{aHome}"
    def __read(self, aPath):
        subspace, extension = os.path.splitext(aPath.replace(f"{self.home}/", ''))
        if (extension == '.py'):
            loader = importlib.machinery.SourceFileLoader('module', aPath)
            spec = importlib.util.spec_from_loader('module', loader)
            value = importlib.util.module_from_spec(spec)
            loader.exec_module(value)
        else:
            value = Path(aPath).read_text().strip()
        self.set(subspace.replace('/', '.'), value)

