
from pylods.deserialize import Typed, EventBasedDeserializer, Module
from pylodsjson.pylodsjson import JsonParser, JsonObjectMapper, JSONDictionary
import io
from pylods.decorators import rename_attr, use_serializer, type_attr, order_attr
from pylods.serialize import Serializer
from pylods.backend.pylodsp.mapper import PyObjectMapper
from pylods.backend.pylodsc.mapper import CObjectMapper
from pylods.mapper import ObjectMapper
from _io import BytesIO


backend = PyObjectMapper

class Job(Typed):
    
    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        

@type_attr('jobs', Job)
@order_attr('firstname',1)
@order_attr('lastname',2)
@order_attr('jobs',3)
class PersonInfo(Typed):
    
    def __init__(self, firstname=None, lastname=None, jobs=None):
        self.firstname = firstname
        self.lastname = lastname
        self.jobs = jobs
    
    def __str__(self):
        return "{PersonInfo first: " + self.firstname + ", last: " + self.lastname + ", jobs: " + str(self.jobs) + "}";
    
# PersonInfo.register_type("jobs", Job)

class TestClass(Typed):
    
    def __init__(self, codes=None, value=None, obj=None):
        self.codes = codes
        self.value = value
        self.obj = obj
    
    def __str__(self):
        return "{TestClass name: " + str(self.codes) + ", value: " + str(self.value) + ", obj: " + str(self.obj) + " }";

TestClass.register_type('obj', PersonInfo)



class PersonInfoDeserializer(EventBasedDeserializer):
     
    def deserialize(self, events, pdict, ctxt):
        mapper = ObjectMapper(pdict.mapper_backend)
        print(mapper.read_obj_property_name(events))        
        firstname = mapper.read_value(events)
        print("fn "+firstname)
        mapper.read_obj_property_name(events)
        lastname = mapper.read_value(events)
        print("ln "+str(lastname))
        mapper.read_obj_property_name(events)
        jobs = mapper.read_array(events,cls=Job)
        return PersonInfo(firstname, lastname, jobs)
#     
    
class Test2Serializer(Serializer):
    
    def serialize(self, gen, obj, outstream):
        gen.write_object_start(1, outstream)
        
        gen.write_object_field('m', obj._y, outstream)
        gen.write_object_field_separator('x', obj.x, outstream);
        gen.write_object_field('x', obj.x, outstream)
        
        gen.write_object_end(1, outstream)
    

@use_serializer(Test2Serializer)    
@rename_attr('_y', 'm')
@rename_attr('x', 'l')
class Test2:
    
    def __init__(self, x=None, _y=None):
        self.x = x
        self._y = _y
        
    def __str__(self):
        return str(self.__dict__)
        
    
    
    
mod = Module()
mod.add_deserializer(PersonInfo, PersonInfoDeserializer())

        

x = PersonInfo()
y = Typed()
# print(TestClass._types)
 
f = open("../samples/sample2.json", 'r')
    

parser = JsonParser()
mapper = JsonObjectMapper(backend(JSONDictionary()))
mapper.register_module(mod)

events = parser.parse(f)
res = mapper.read_obj(events, TestClass)

    




print("************************************* \n" + str(res))
print(res.codes)
print(res.obj)
 
res.x = 5
res._y = 4
 
 
print("???????????????")
out = io.BytesIO()
t2 = Test2(1, 2)
mapper = mapper.copy()
mapper.write(t2, out)
print(out.getvalue())
out.seek(0)
parser = JsonParser()
print("???????????????2")
mapper = JsonObjectMapper(backend(JSONDictionary()));
t2out = mapper.read_obj(parser.parse(out), cls=Test2)
print(t2out)
 
print("&&&&&&&&&&&&&&&&&&&&&&&&&")
 
out = BytesIO();
parser = JsonParser()
mapper = JsonObjectMapper(backend(JSONDictionary()))
mapper.write([{"x":1}, {"x":1}], out)
out.seek(0)
events = parser.parse(out)
res = mapper.read_array(events, cls=dict)
print(res)

print("&&&&&&&&&&&&&&&&&&&&&&&&&2")

pi =PersonInfo("test", "Test", [Job("J1", "L1")]);
out = BytesIO();
parser = JsonParser()
mapper = JsonObjectMapper(backend(JSONDictionary()))
m = Module()
m.add_deserializer(PersonInfo, PersonInfoDeserializer())
mapper.register_module(m)
mapper.write(pi, out)
out.seek(0)
events = parser.parse(out)
res = mapper.read_obj(events, cls=PersonInfo)
print(res)