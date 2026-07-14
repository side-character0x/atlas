import re

class Interface:
    def __init__(self,Route):
        self.route=Route
    def query(self):
        while True:
            cmd=input("Enter the command:")
            return cmd
    def error_handle(self,error):
        print(error)
    def workspace_query(self):
        print("REMAINDERS:\n1.For executable files, enter the name. (chrome,microsoft edge.....)\n2.For websites,enter the path. (https://......)\n3.Assign type 'url' for websites and 'app' for apps.\n4.Enter the name of browser where the url will be needed to load and leave blank to use default browser.\n5.Only one resource in one line\n6.Type 'End' to end input.")
        resources=[]
        while True:
            resource=input("Enter your workspace resources:")
            if resource.lower()=="end":
                break
            while True:
                Type=input('Enter the type of resource:').lower()
                if Type in ['app','url']:
                    break
                else:
                    print("Invalid type")
            if Type=="url":
                browser=input("Enter your preffered browser:")
                if not browser:
                    browser=None
            else:
                browser=None
            response=self.route.validity(resource,Type,browser)
            if response:
                resources.append([resource,Type,browser])
            else:
                print("App or URL is either invalid or not registered in the device")
        return resources
    def choice_query(self):
        while True:
            choice=input("Delete any resources?(y/n)").lower()
            if choice=="y":
                return True
            elif choice=="n":
                return False
            else:
                print("Invalid input!")
    def show_resources(self,resources):
        for data in resources:
            print(f"{data[3]}.{data[0]}")
    def delete_query(self):
        print("Enter the corresponding symbol of resource to be deleted.\nComma or space seperation is required!")
        choice=input("Enter here:\n>")
        symbols=re.split(r"[,\s]+",choice.strip())
        return symbols
    def exit_response(self):
        print("Type Exit to close.")