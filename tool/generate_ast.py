import sys

class GenerateAst():
    def __init__(self):
        args: list = sys.argv

        if len(args) == 1:
            print("Usage: generate_ast <output directory>")
            exit()
        
        output_dir: str = args[1]
        self.define_ast(output_dir, "Expr", [
            "Binary   : left, operator, right",
            "Grouping : expression",
            "Literal  : value",
            "Unary    : operator, right"
        ])

    def define_ast(self, output_dir: str, base_name: str, types: list[str]):
        path: str = f"{output_dir}/{base_name}.py"
        writer = open(path, "w")

        #Imports
        writer.write("from abc import ABC, abstractmethod\n")
        writer.write("\n")

        self.define_base_class(writer, base_name)

        #AST classes
        for type in types:
            class_name: str = type.split(":")[0].strip()
            fields: str = type.split(":")[1].strip()
            self.define_type(writer, base_name, class_name, fields)

        self.define_visitor(writer, base_name, types)
        writer.close()
    
    @staticmethod
    def define_base_class(writer, base_name: str):
        writer.write(f"class {base_name}(ABC):\n")
        #Base accept method
        writer.write("    @abstractmethod\n")
        writer.write("    def accept(self, visitor):\n")
        writer.write("        pass\n")
        writer.write("\n")

    @staticmethod
    def define_visitor(writer, base_name: str, types: list[str]):
        writer.write("class Visitor(ABC):\n")

        for type in types:
            type_name: str = type.split(":")[0].strip()
            writer.write("    @abstractmethod\n")
            writer.write(f"    def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}:  {type_name}):\n")
            writer.write("        pass\n")
        
        writer.write("\n")

    @staticmethod
    def define_type(writer, base_name: str, class_name: str, field_list: str):
        writer.write(f"class {class_name}({base_name}):\n")

        #Constructor
        writer.write(f"    def __init__(self, {field_list}):\n")

        #Store paramaters in fields
        fields: list[str] = field_list.split(", ")
        for field in fields:
            name: str = field.strip()
            writer.write(f"        self.{name} = {name}\n")

        writer.write("\n")
        writer.write("    def accept(self, visitor):\n")
        writer.write(f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n")
        writer.write("\n")

if __name__ == "__main__":
    GenerateAst()