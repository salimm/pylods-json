
from pylods.deserialize import Typed, EventBasedDeserializer
from pylodsjson.pylodsjson import JsonParser, JsonObjectMapper
from pylods.mapper import ObjectMapper, Module
import io
from pylods.decorators import rename_attr
from pylods.serialize import Serializer



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
        return "{ first: " + self.firstname + ", last: " + self.lastname + ", jobs: " + str(self.jobs) + "}";
    
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
        mapper = ObjectMapper(pdict, events)
        mapper.read_obj_propery_name()
        firstname = mapper.read_value()
        mapper.read_obj_propery_name()
        lastname = mapper.read_value()
        mapper.read_obj_propery_name()
        jobs = mapper.read_array(cls=Job)
        return PersonInfo(firstname, lastname, jobs)
    
    def handled_class(self):
        return PersonInfo
    
    
@rename_attr('_y', 'm')
@rename_attr('x', 'l')
class Test2:
    
    def __init__(self, x=None, _y=None):
        self.x = x
        self._y = _y
        
    def __str__(self):
        return str(self.__dict__)
        
    
class Test2Serializer(Serializer):
    
    def serialize(self, gen, obj, outstream):
        gen.write_object_start(1, outstream)
        
        gen.write_object_field('m', obj._y, outstream)
        
        gen.write_object_end(1, outstream)
    
    def handled_class(self):
        return Test2
    
    
mod = Module()
mod.add_deserializer(PersonInfoDeserializer())
mod.add_serializer(Test2Serializer())
    
        

x = PersonInfo()
y = Typed()
print(TestClass._types)
 
f = open("../sample2.json", 'r')


parser = JsonParser()
mapper = JsonObjectMapper(parser.parse(f))
mapper.register_module(mod)


res = mapper.read_obj(TestClass)

    
    



print(res)
print(res.codes)
print(res.obj)

res.x = 5

res._y = 4

out = io.BytesIO()

t2 = Test2(1, 2)


mapper.write(t2, out)
print(out.getvalue())
out.seek(0)

parser = JsonParser()
mapper = JsonObjectMapper(parser.parse(out))
t2out = mapper.read_obj(Test2)

print(t2out)



