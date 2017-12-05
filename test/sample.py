

from pylods.core import Typed, Module
from pylodsjson.pylodsjson import JsonParser, JsonObjectMapper
from pylods.serialize import Deserializer, EventBasedDeserializer
import new
import parser



class Job(Typed):
    
    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        

class PersonInfo(Typed):
    
    def __init__(self, firstname=None, lastname=None, jobs=None):
        self.firstname = firstname
        self.lastname = lastname
        self.jobs = jobs
    
    def __str__(self):
        return "{ first: "+self.firstname +", last: "+self.lastname +", jobs: "+ str(self.jobs)+"}";
    
PersonInfo.register_type("jobs", Job)

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
# mapper.register_module(mod)


res = mapper.read_obj(TestClass)
 



print(res)
print(res.codes)
print(res.obj)

