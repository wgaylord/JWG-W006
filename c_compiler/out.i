{
  "program": [
    [
      "defVar",
      {
        "parent": "test",
        "name": "serial",
        "type": "pointer_char",
        "init": [
          [
            "loadConst",
            3221225472
          ]
        ],
        "local": false
      }
    ],
    [
      "defVar",
      {
        "parent": "test",
        "name": "serial2",
        "type": "char",
        "init": [
          [
            "loadConst",
            2
          ]
        ],
        "local": false
      }
    ],
    [
      "defVar",
      {
        "parent": "test",
        "name": "TestString",
        "type": "array_char",
        "init": [
          [
            "defArray",
            "This is a test"
          ]
        ],
        "local": false
      }
    ],
    [
      "funcDef",
      "main",
      []
    ],
    [
      "loadVarAsArg",
      "TestString"
    ],
    [
      "callFunc",
      "printString"
    ],
    [
      "return"
    ],
    [
      "funcDef",
      "printString",
      [
        {
          "name": "str",
          "type": "pointer_char"
        }
      ]
    ],
    [
      "defVar",
      {
        "parent": "printString",
        "name": "index",
        "type": "short",
        "init": [
          [
            "loadConst",
            0
          ]
        ],
        "local": true
      }
    ],
    [
      "while_cond",
      "printString"
    ],
    [
      "arrayAccess",
      "index",
      "str"
    ],
    [
      "binOpLeft"
    ],
    [
      "loadConst",
      0
    ],
    [
      "binOpRight"
    ],
    [
      "binOp",
      "!="
    ],
    [
      "while",
      "printString"
    ],
    [
      "arrayAccess",
      "index",
      "str"
    ],
    [
      "loadVar",
      "serial"
    ],
    [
      "assign"
    ],
    [
      "loadVar",
      "index"
    ],
    [
      "binOpLeft"
    ],
    [
      "loadConst",
      1
    ],
    [
      "binOpRight"
    ],
    [
      "binOp",
      "+"
    ],
    [
      "binOpLeft"
    ],
    [
      "loadConst",
      3
    ],
    [
      "binOpRight"
    ],
    [
      "binOp",
      "+"
    ],
    [
      "loadVar",
      "index"
    ],
    [
      "assign"
    ],
    [
      "while_end",
      "printString"
    ],
    [
      "return"
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