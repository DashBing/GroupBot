# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Test.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nTest.proto\x12\nTest.proto\"?\n\x03Msg\x12\t\n\x01n\x18\x01 \x01(\x05\x12\x1d\n\x02ss\x18\x05 \x03(\x0b\x32\x11.Test.proto.Msg.S\x1a\x0e\n\x01S\x12\t\n\x01n\x18\x01 \x01(\x05\x62\x06proto3')



_MSG = DESCRIPTOR.message_types_by_name['Msg']
_MSG_S = _MSG.nested_types_by_name['S']
Msg = _reflection.GeneratedProtocolMessageType('Msg', (_message.Message,), {

  'S' : _reflection.GeneratedProtocolMessageType('S', (_message.Message,), {
    'DESCRIPTOR' : _MSG_S,
    '__module__' : 'Test_pb2'
    # @@protoc_insertion_point(class_scope:Test.proto.Msg.S)
    })
  ,
  'DESCRIPTOR' : _MSG,
  '__module__' : 'Test_pb2'
  # @@protoc_insertion_point(class_scope:Test.proto.Msg)
  })
_sym_db.RegisterMessage(Msg)
_sym_db.RegisterMessage(Msg.S)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MSG._serialized_start=26
  _MSG._serialized_end=89
  _MSG_S._serialized_start=75
  _MSG_S._serialized_end=89
# @@protoc_insertion_point(module_scope)
