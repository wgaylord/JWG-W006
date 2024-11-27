from pycparser import c_parser, parse_file, c_ast
from pprint import pprint

source_name = "test"

ast = parse_file("test.c", use_cpp=False)

types = {"int":{"name":"int","size":4},"short":{"name":"short","size":2},"char":{"name":"char","size":1},"pointer":{"name":"pointer","size":4}}

# Format   ["op",....,left_arg,right_arg,out_arg]

reg_num = 0

def getTemp():
    global reg_num
    reg_num += 1
    return "x"+str(reg_num)


class Evaluator:

    def __init__(self,name = "",parent=None):
        self.name = name
        self.parent = parent
        self.code = []
        self.locals = {}
      
      
        
    def evaluate(self,node):
        returnValue = []
    
        if isinstance(node,c_ast.FileAST):
            returnValue1 = []

            for x in node.ext:
                nodeEvaluator = Evaluator(self.name,self)
                data = nodeEvaluator.evaluate(x)
                returnValue1.extend(data)
            returnValue.append(["globalInfo",self.locals,"","",""])
            returnValue.extend(returnValue1)
        if isinstance(node,c_ast.Decl):
            decl = self.evalDecl(node)
            if decl != None:
                if decl["local"]:
                    self.locals[decl["name"]] = decl
                else:
                    self.parent.locals[decl["name"]] = decl
                if decl["init"]:
                    returnValue.append(decl["init"][-1])
                else: 
                    returnValue.append(["const",0,"",getTemp()])
                #print("move",returnValue[-1][-1],"",decl["name"])
                returnValue.append(["move",returnValue[-1][-1],"",decl["name"]])
            
        elif isinstance(node,c_ast.Constant):
            returnValue.append(self.evalConst(node))
        elif isinstance(node,c_ast.FuncDef):

            funcName,funcReturn,funcArgs = self.evalFuncDecl(node.decl)
            returnValue.append(["funcDef",funcName,funcArgs,"","",""])
            nodeEvaluator = Evaluator(funcName,self)
            funcBody = nodeEvaluator.evaluate(node.body)
            returnValue.append(["localInfo",self.locals,"","",""])
            returnValue.extend(funcBody)
            returnValue.append(["return","","",""])
            
        elif isinstance(node,c_ast.Compound):
            if node.block_items:
                for x in node.block_items:
                    returnValue.extend(self.evaluate(x))
        elif isinstance(node,c_ast.FuncCall):
            name = ""
            if isinstance(node.name,c_ast.ID):
                name = node.name.name
            args = []
            for x in node.args.exprs:
                if isinstance(x,c_ast.ID):
                    args.append(x.name)
                else:
                    returnValue.extend(self.evaluate(x))
                    args.append(returnValue[-1][-1])
            returnValue.append(["funcCall",name,args,"",getTemp()])
        elif isinstance(node,c_ast.Return):
            data = self.evaluate(node.expr)
            returnValue.extend(data)
            returnValue.append(["return","","",data[-1]])
        elif isinstance(node,c_ast.ID):
            returnValue.append(["ID","","",node.name])
        elif isinstance(node,c_ast.ArrayRef):
            name = self.evaluate(node.name)
            subscript = self.evaluate(node.subscript)
            returnValue.append(["arrayAccess",name[-1][-1],subscript[-1][-1],getTemp()])
            #print(name,subscript)
            
        elif isinstance(node,c_ast.BinaryOp):
            #print(node.left,node.op,node.right)
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            returnValue.extend(left)
            returnValue.extend(right)
            returnValue.append(["binOp",node.op,left[-1][-1],right[-1][-1],getTemp()])
        elif isinstance(node,c_ast.Assignment):
            r = self.evaluate(node.rvalue)
            l = self.evaluate(node.lvalue)
            returnValue.extend(r)
            returnValue.extend(l)
            if l[-1][0] == "addressOf":
                returnValue.append(["store",r[-1][-1],"",l[-1][-1]])
            elif l[-1][0] == "arrayAccess":
                l[-1][0] = "arrayIndex"
                returnValue.append(["storeArray",r[-1][-1],"",l[-1][-1]])
            else:
                returnValue.append(["move",r[-1][-1],"",l[-1][-1]])
        elif isinstance(node,c_ast.While):
            cond = self.evaluate(node.cond)
            returnValue.append(["whileCond","","",""])
            returnValue.extend(cond)
            op = returnValue.pop()
            returnValue.append(["cmp",op[2],op[3],""])
            returnValue.append(["whileTest",op[1],"","",""])
            returnValue.append(["whileStart","","",""])
            nodeEvaluator = Evaluator(self.name,self)
            data = nodeEvaluator.evaluate(node.stmt)
            returnValue.append(["localInfo",nodeEvaluator.locals,"","",""])
            returnValue.extend(data)
            returnValue.append(["whileEnd","","",""])

        elif isinstance(node,c_ast.If):
            cond = self.evaluate(node.cond)
            returnValue.extend(cond)
            op = returnValue.pop()
            returnValue.append(["cmp",op[2],op[3],""])
            returnValue.append(["ifTest",op[1],"","",""])
            returnValue.append(["ifTrue","","",""])
            if node.iftrue:
                nodeEvaluator = Evaluator(self.name,self)
                data = nodeEvaluator.evaluate(node.iftrue)
                returnValue.append(["localInfo",nodeEvaluator.locals,"","",""])
                returnValue.extend(data)
            if node.iffalse:
                returnValue.append(["ifFalse","","",""])
                data = nodeEvaluator.evaluate(node.iffalse)
                returnValue.append(["localInfo",nodeEvaluator.locals,"","",""])
                returnValue.extend(data)
            returnValue.append(["ifEnd","","",""])

            
            
        elif isinstance(node,c_ast.UnaryOp):
            nodeEvaluator = Evaluator(self.name,self)
            if node.op == "*":
                returnValue.extend(nodeEvaluator.evaluate(node.expr))
                returnValue.append(["addressOf","","",returnValue[-1][-1]])
        else:
            pass
            print("undefined",node)
        #print(returnValue)
        return returnValue
       


    def evalDecl(self,node):
        declType = self.evalType(node.type)
        declName = node.name
        if declType != "func":
            var = {"parent":self.parent.name,"name":declName,"type":declType,"init":self.evaluate(node.init),"local":self.parent.name != source_name}
            
            return var

     
    def evalType(self,node):
        typeName = ""
        if isinstance(node,c_ast.PtrDecl):
            typeName = "pointer_" + self.evalType(node.type)
            types[typeName] = types["pointer"]
            return typeName
        elif isinstance(node,c_ast.TypeDecl):
            typeName = self.evalType(node.type)
        elif isinstance(node,c_ast.IdentifierType):
            typeName = node.names[0]
        elif isinstance(node,c_ast.FuncDecl):
            typeName = "func"
        elif isinstance(node,c_ast.ArrayDecl):
            typeName = "array_" + self.evalType(node.type)
            types[typeName] = types["pointer"] 
        return typeName

    def evalConst(self,node):
        if node.type == "int":
            if "x" in node.value:
                return ["const",int(node.value,16),"",getTemp()]
            else:
                return ["const",int(node.value),"",getTemp()]
        if node.type == "string":
            return ["constArray",node.value[1:-1],"",getTemp()]
            
    def evalFuncDecl(self,node):
        funcName = node.name
        funcReturn = self.evalType(node.type.type)
        funcArgs = []
        if node.type.args != None:
            for x in node.type.args.params:
                parmaName = x.name
                parmaType = self.evalType(x.type)
                funcArgs.append({"name":parmaName,"type":parmaType})
                
        
        return funcName,funcReturn,funcArgs
        
program = []
program.extend(Evaluator(source_name).evaluate(ast))

print(len(program))
output = {"program":program,"types":types}

import json
open("out.i","w+").write(json.dumps(output,indent=1))

