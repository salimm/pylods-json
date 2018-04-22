
from pylods.deserialize import Typed, EventBasedDeserializer
from pylodsjson.pylodsjson import JsonParser, JsonObjectMapper, JSONDictionary
import io
from pylods.decorators import rename_attr, use_serializer, type_attr
from pylods.serialize import Serializer
from pylods.backend.pylodsp.mapper import PyObjectMapper
from pylods.backend.pylodsc.mapper import CObjectMapper
from pylods.mapper import ObjectMapper



class Job(Typed):
    
    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        

@type_attr('jobs', Job)
class PersonInfo(Typed):
    
    def __init__(self, firstname=None, lastname=None, jobs=None):
        self.firstname = firstname
        self.lastname = lastname
        self.jobs = jobs
    
    def __str__(self):
        return "{ first: " + self.firstname + ", last: " + self.lastname + ", jobs: " + str(self.jobs) + "}";
    
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
        mapper = ObjectMapper(pdict)
        mapper.read_obj_propery_name(events)
        firstname = mapper.read_value(events)
        mapper.read_obj_propery_name(events)
        lastname = mapper.read_value(events)
        mapper.read_obj_propery_name(events)
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
        
    
    
    
# mod = Module()
# mod.add_deserializer(PersonInfo, PersonInfoDeserializer())

        

x = PersonInfo()
y = Typed()
# print(TestClass._types)
 
f = open("../sample2.json", 'r')
    

parser = JsonParser()
mapper = JsonObjectMapper(CObjectMapper(JSONDictionary()))
# mapper.register_module(mod)

events = parser.parse(f)
res = mapper.read_obj(events, TestClass)

    




print("************************************* \n" + str(res))
print(res.codes)
print(res.obj)

res.x = 5

res._y = 4

out = io.BytesIO()

t2 = Test2(1, 2)

mapper = mapper.copy()
mapper.write(t2, out)
print(out.getvalue())
out.seek(0)

parser = JsonParser()
mapper = JsonObjectMapper(PyObjectMapper(JSONDictionary()));
t2out = mapper.read_obj(parser.parse(out), Test2)

print(t2out)



