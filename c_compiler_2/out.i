{
 "program": [
  [
   "globalInfo",
   {
    "serial": {
     "parent": "test",
     "name": "serial",
     "type": "pointer_char",
     "init": [
      [
       "const",
       3221225472,
       "",
       "x1"
      ]
     ],
     "local": false
    },
    "serial2": {
     "parent": "test",
     "name": "serial2",
     "type": "char",
     "init": [
      [
       "const",
       2,
       "",
       "x2"
      ]
     ],
     "local": false
    },
    "TestString": {
     "parent": "test",
     "name": "TestString",

"type": "array_char",
     "init": [
      [
       "constArray",
       "This is a test",
       "",
       "x3"
      ]
     ],
     "local": false
    }
   },
   "",
   "",
   ""
  ],
  [
   "const",
   3221225472,
   "",
   "x1"
  ],
  [
   "move",
   "x1",
   "",
   "serial"
  ],
  [
   "const",
   2,
   "",
   "x2"
  ],
  [
   "move",
   "x2",
   "",
   "serial2"
  ],
  [
   "constArray",
   "This is a test",
   "",
   "x3"
  ],
  [
   "move",
   "x3",
   "",
   "TestString"
  ],
  [
   "funcDef",
   "main",
   [],
   "",
   "",
   ""
  ],
  [
   "localInfo",
   {},
   "",
   "",
   ""
  ],
  [
   "funcCall",
   "printString",
   [
    "TestString"
   ],
   "",
   "x4"
  ],
  [
   "return",
   "",
   "",
   ""
  ],
  [
   "funcDef",
   "printString",
   [
    {
     "name": "str",
     "type": "pointer_char"
    }
   ],
   "",
   "",
   ""
  ],
  [
   "localInfo",
   {
    "index": {
     "parent": "test",
     "name": "index",
     "type": "short",
     "init": [
      [
       "const",
       0,
       "",
       "x5"
      ]
     ],
     "local": false
    }
   },
   "",
   "",
   ""
  ],
  [
   "const",
   0,
   "",
   "x5"
  ],
  [
   "move",
   "x5",
   "",
   "index"
  ],
  [
   "whileCond",
   "",
   "",
   ""
  ],
  [
   "arrayAccess",
   "str",
   "index",
   "x6"
  ],
  [
   "const",
   0,
   "",
   "x7"
  ],
  [
   "cmp",
   "x6",
   "x7",
   ""
  ],
  [
   "whileTest",
   "!=",
   "",
   "",
   ""
  ],
  [
   "whileStart",
   "",
   "",
   ""
  ],
  [
   "localInfo",
   {},
   "",
   "",
   ""
  ],
  [
   "arrayAccess",
   "str",
   "index",
   "x9"
  ],
  [
   "const",
   10,
   "",
   "x10"
  ],
  [
   "cmp",
   "x9",
   "x10",
   ""
  ],
  [
   "ifTest",
   "==",
   "",
   "",
   ""
  ],
  [
   "ifTrue",
   "",
   "",
   ""
  ],
  [
   "localInfo",
   {},
   "",
   "",
   ""
  ],
  [
   "const",
   13,
   "",
   "x12"
  ],
  [
   "ID",
   "",
   "",
   "serial"
  ],
  [
   "addressOf",
   "",
   "",
   "serial"
  ],
  [
   "store",
   "x12",
   "",
   "serial"
  ],
  [
   "const",
   10,
   "",
   "x13"
  ],
  [
   "ID",
   "",
   "",
   "serial"
  ],
  [
   "addressOf",
   "",
   "",
   "serial"
  ],
  [
   "store",
   "x13",
   "",
   "serial"
  ],
  [
   "ifFalse",
   "",
   "",
   ""
  ],
  [
   "localInfo",
   {},
   "",
   "",
   ""
  ],
  [
   "ID",
   "",
   "",
   "serial"
  ],
  [
   "addressOf",
   "",
   "",
   "serial"
  ],
  [
   "arrayIndex",
   "str",
   "index",
   "x14"
  ],
  [
   "storeArray",
   "serial",
   "",
   "x14"
  ],
  [
   "ID",
   "",
   "",
   "index"
  ],
  [
   "const",
   1,
   "",
   "x15"
  ],
  [
   "binOp",
   "+",
   "index",
   "x15",
   "x16"
  ],
  [
   "const",
   3,
   "",
   "x17"
  ],
  [
   "binOp",
   "+",
   "x16",
   "x17",
   "x18"
  ],
  [
   "ID",
   "",
   "",
   "index"
  ],
  [
   "move",
   "x18",
   "",
   "index"
  ],
  [
   "ifEnd",
   "",
   "",
   ""
  ],
  [
   "whileEnd",
   "",
   "",
   ""
  ],
  [
   "return",
   "",
   "",
   ""
  ]
 ],
 "types": {
  "int": {
   "name": "int",
   "size": 4
  },
  "short": {
   "name": "short",
   "size": 2
  },
  "char": {
   "name": "char",
   "size": 1
  },
  "pointer": {
   "name": "pointer",
   "size": 4
  },
  "pointer_char": {
   "name": "pointer",
   "size": 4
  },
  "array_char": {
   "name": "pointer",
   "size": 4
  }
 }
}
