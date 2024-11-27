from pycparser import c_parser, parse_file, c_ast
from pprint import pprint

source_name = "test"

ast = parse_file("test.c", use_cpp=False)

types = {"int":{"name":"int","size":4},"short":{"name":"short","size":2},"char":{"name":"char","size":1},"pointer":{"name":"pointer","size":4}}

class Evaluator:

    def __init__(self,name = "",parent=None):
        self.name = name
        self.parent = parent
        self.code = []
        
        
    def evaluate(self,node):
        returnValue = []
    
        if isinstance(node,c_ast.FileAST):
            for x in node.ext:
                nodeEvaluator = Evaluator(self.name,self)
                returnValue.extend(nodeEvaluator.evaluate(x))
        elif isinstance(node,c_ast.Decl):
            #print(node)
            var = self.evalDecl(node)
            if var:
                returnValue.append(["defVar",var])
        elif isinstance(node,c_ast.Constant):
            returnValue.append(self.evalConst(node))
        elif isinstance(node,c_ast.FuncDef):
            #print(node)
            
            funcName,funcReturn,funcArgs = self.evalFuncDecl(node.decl)
            returnValue.append(["funcDef",funcName,funcArgs])
            nodeEvaluator = Evaluator(funcName)
            funcBody = nodeEvaluator.evaluate(node.body)
            returnValue.extend(funcBody)
            returnValue.append(["return"])
        elif isinstance(node,c_ast.Compound):
            if node.block_items:
                for x in node.block_items:
                    nodeEvaluator = Evaluator(self.name,self)
                    returnValue.extend(nodeEvaluator.evaluate(x))
        elif isinstance(node,c_ast.FuncCall):
            nodeEvaluator = Evaluator(self.name,self)
            for x in node.args.exprs:
                returnValue.extend(nodeEvaluator.evaluate(x))
                returnValue.append(["setArg"])
            returnValue.append(["callFunc",node.name.name])
            
            
        elif isinstance(node,c_ast.ID):
            returnValue.append(["loadVar",node.name])
            
        elif isinstance(node,c_ast.Return):
            nodeEvaluator = Evaluator(self.name,self)
            returnValue.extend(nodeEvaluator.evaluate(node.expr))
            returnValue.append(["return"])
            
        elif isinstance(node,c_ast.While):
            #print(node)
            nodeEvaluator = Evaluator(self.name+".while",self)
            returnValue.append(["while_cond",self.name])
            returnValue.extend(nodeEvaluator.evaluate(node.cond))
            returnValue.append(["while",self.name])
            returnValue.extend(nodeEvaluator.evaluate(node.stmt))
            returnValue.append(["while_end",self.name])
        
        elif isinstance(node,c_ast.BinaryOp):
            nodeEvaluator = Evaluator(self.name,self)
            returnValue.extend(nodeEvaluator.evaluate(node.left))
            returnValue.append(["binOpLeft"])
            returnValue.extend(nodeEvaluator.evaluate(node.right))
            returnValue.append(["binOpRight"])
            returnValue.append(["binOp",node.op])
        elif isinstance(node,c_ast.ArrayRef):
            print(node)
            nodeEvaluator = Evaluator(self.name,self)
            returnValue.extend(nodeEvaluator.evaluate(node.subscript))
            returnValue.extend(nodeEvaluator.evaluate(node.name))
            returnValue.append(["arrayAccess"])
            print(returnValue)
        elif isinstance(node,c_ast.Assignment):
            nodeEvaluator = Evaluator(self.name,self)
            returnValue.extend(nodeEvaluator.evaluate(node.rvalue))
            returnValue.extend(nodeEvaluator.evaluate(node.lvalue))
            returnValue.append(["assign"])
        elif isinstance(node,c_ast.UnaryOp):
            nodeEvaluator = Evaluator(self.name,self)
            if node.op == "*":
                returnValue.extend(nodeEvaluator.evaluate(node.expr))
        elif isinstance(node,c_ast.If):
            nodeEvaluator = Evaluator(self.name+".while",self)
            returnValue.append(["if_cond",self.name])
            returnValue.extend(nodeEvaluator.evaluate(node.cond))
            if node.iftrue:
                returnValue.append(["if_true",self.name])
                returnValue.extend(nodeEvaluator.evaluate(node.iftrue))
            if node.iffalse:
                returnValue.append(["if_false",self.name])
                returnValue.extend(nodeEvaluator.evaluate(node.iffalse))
            returnValue.append(["if_End",self.name])
        else:
            print("undefined",node)
        print(returnValue)
        return returnValue
       


    def evalDecl(self,node):
        declType = self.evalType(node.type)
        declName = node.name
        if declType != "func":
            var = {"parent":self.parent.name,"name":declName,"type":declType,"init":self.evalInit(node.init),"local":self.parent.name != source_name}
            
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

    def evalInit(self,node):
        nodeEvaluator = Evaluator(self.name,self)
        return nodeEvaluator.evaluate(node)
        
    def evalConst(self,node):
        if node.type == "int":
            if "x" in node.value:
                return ["loadConst",int(node.value,16)]
            else:
                return ["loadConst",int(node.value)]
        if node.type == "string":
            return ["defArray",node.value[1:-1]]
            
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
pprint(program)


def optimizeFuncCall(prog):
    index = 0
    output = []
    
    while index < len(prog):
        if prog[index][0] == "loadVar" and index+1 < len(prog):
            if prog[index+1][0] == "setArg":
                output.append(["loadVarAsArg",prog[index][1]])
                index += 1
            elif index+2 < len(prog) and prog[index+2][0] == "arrayAccess":
                output.append(["arrayAccess",prog[index][1],prog[index+1][1]])
                index += 2
            else:
                output.append(prog[index])
        elif prog[index][0] == "loadConst" and index+1 < len(prog):
            if prog[index+1][0] == "setArg":
                output.append(["loadConstAsArg",prog[index][1]])
                index += 1
            else:
                output.append(prog[index])
            pass
        else:
            output.append(prog[index])
            
        index += 1
            
    return output


def optimizeProgram(prog):

    prog = optimizeFuncCall(prog)
    return prog


program1 = optimizeProgram(program)

pprint(program1)
output = {"program":program1,"types":types}

import json
open("out.i","w+").write(json.dumps(output,indent=2))

