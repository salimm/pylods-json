

from pylods.core import Typed, Module
from pylodsjson.pylodsjson import JsonParser, JsonObjectMapper
from pylods.serialize import Deserializer, EventBasedDeserializer
import new
import parser



class PersonInfo(Typed):
    
    def __init__(self, firstname=None, lastname=None, jobs=None):
        self.firstname = firstname
        self.lastname = lastname
        self.jobs = jobs
        
    

class TestClass(Typed):
    
    def __init__(self, codes=None, value=None, obj=None):
        self.codes = codes
        self.value = value
        self.obj = obj
    
    def __str__(self):
        return "{TestClass name: " + str(self.codes) + ", value: " + str(self.value) + ", obj: " + str(self.obj) + " }";


TestClass.register_type('obj', PersonInfo)


class PersonInfoDeserializer(EventBasedDeserializer):
    
    def deserialize(self, events, pdict):
        return "test"
    
    def handled_class(self):
        return PersonInfo
    
    

mod = Module()
mod.add_deserializer(PersonInfoDeserializer())
    
        

x = PersonInfo()
y = Typed()
print(TestClass._types)
 
f = open("../sample2.json", 'r')


parser = JsonParser()
mapper = JsonObjectMapper(parser.parse(f))
mapper.register_module(mod)


res = mapper.parse_obj(TestClass)
 



print(res)
print(res.codes)
print(res.obj)

