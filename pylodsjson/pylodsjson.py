'''
Created on Nov 26, 2017

@author: Salim
'''
from pylods.core import Parser, ObjectMapper
from pylods.dict import Dictionary
import ijson


class JSONDictionary(Dictionary):
    
    def gen_events(self, instream):
        '''
            generates events from parsing the input stream
        '''
        return ijson.parse(instream)
    
    def is_obj_start(self, event):
        '''
            indicates if the given or a tuple representing an start of object event
            :param event:
        '''
        return event[1] == u'start_map'
    
    def is_obj_end(self, event):
        '''
            indicates if the given or a tuple representing an end of object event
            :param event:
        '''
        return event[1] == u'end_map'
        
    def is_value(self, event):
        '''
            indicates if the given or tuple representing an event that represents a raw value
            :param event:
        '''
        return event[2] is not None
        
    def is_obj_property_name(self, event):
        '''
         indicates if the given event or tuple representing an event is a property name. 
          This library expects to receive the value of the property next. If this value is 
          an object or array, start event for an array or map is expected.
          
        :param event:
        '''
        return event[1] == u'map_key'
         
    def is_array_start(self, event):
        '''
            indicates if the given or tuple representing an event that indicates start of an array
            :param event:
        '''
        return event[1] == u'start_array'
    
    def is_array_end(self, event):
        '''
            indicates if the given or tuple representing an event that indicates end of an array
            :param event:
        '''
        return event[1] == u'end_array'
    
    def read_value(self, event):
        '''
            Returns the value of an ijson event 
        '''
        return event[2]
    
    


class JsonParser(Parser):
    '''
        Json Parser extends PylodsParser while using a JsonDictionary
    '''
    
    
    def __init__(self):
        Parser.__init__(self, JSONDictionary())
        


class JsonObjectMapper(ObjectMapper):
    '''
        ObjectMapper for JSON
    '''
    
    
    def __init__(self,  events):
        ObjectMapper.__init__(self,JSONDictionary(),events);
        
