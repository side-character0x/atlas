from discover import Paths
from url_generator import URL

class Route:
    def __init__(self):
        self.paths=Paths()
        self.url=URL()    
    def evaluate(self,cmd):
        try:
            dismantled=cmd.split()
            action,target=dismantled[0].lower(),dismantled[1:]
            suffix=" ".join(target)
            if action=="open":
                resource=self.open_guide(suffix)         
            elif action=="search":
                resource=self.search_guide(target)
            elif action=="create":
                resource=target
            elif action=="load":
                resource=self.load_guide(target)
            elif action=="view":
                resource=self.load_guide(target,view=True)
            elif action=="system":
                resource=suffix
            return action,resource
        except UnboundLocalError:
            return action,False
    def open_guide(self,target):
        path=self.paths.atlasreg(target)
        if path:
            return path
        path=self.paths.windowsreg(target)
        if path:
            return path
        path=self.paths.find_path(target)
        if path:
            return path
        path=target
        return path
    def search_guide(self,target):
        engine,search_query=target[0]," ".join(target[1:])
        url=self.url.generate_query(engine,search_query)
        return url
    def create_guide(self,target,workspace_resources):
        workspace_name=" ".join(target[1:])
        resources=[]
        types=[]
        browser=[]
        for data in workspace_resources:
            resources.append(data[0])
            types.append(data[1])
            browser.append(data[2])
        self.paths.store_data(workspace_name,resources,resource_type=types,type="workspace",browsers=browser)
    def load_guide(self,target,view=False):
        workspace=" ".join(target[1:])
        resources=self.paths.convey_resources(workspace)
        if view:
            if not resources:
                return False
            return resources
        app=[]
        dflt_search=[]
        browse_search=[]
        for resource in resources:
            if resource[1]=="app":
                path=self.open_guide(resource[0]) 
                app.append(path)
            elif resource[1]=="url":      
                if resource[2] is None:
                    dflt_search.append(resource[0])
                else:
                    path=self.open_guide(resource[2])
                    browse_search.append([path,resource[0]])
        return [app, dflt_search,browse_search]
    def validity(self,resource,type,browser):
        if type=="app":
            response=self.open_guide(resource)
            if response and ".exe" not in response:
                response_2=self.paths.winpath_validity(resource)
                if response_2 is None:
                    response=False
        elif type=="url":
            response=self.paths.url_validity(resource)
            if browser is not None:
                response=self.open_guide(browser)
                if response and ".exe" not in response:
                    response_2=self.paths.winpath_validity(browser)
                    if response_2 is None:
                        response=False
        if response:
            return True
        else:
            return False
    def delete_divert(self,resources):
        self.paths.convey_resources(resources,use="delete")




