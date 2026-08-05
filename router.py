from discover import Paths
from url_generator import URL

class Route:
    def __init__(self):
        self.paths=Paths()
        self.url=URL()    
    def evaluate(self,cmd):
        try:
            action_part,target_part=cmd.split(",",1)
            action=action_part.split(":",1)[1].strip().lower()
            target=target_part.split(":",1)[1].strip()
            if action=="open":
                resource=self.open_guide(target)         
            elif action=="search":
                resource=self.search_guide(target)
            elif action=="create":
                resource=target
            elif action=="load":
                resource=self.load_guide(target)
            elif action=="view":
                resource=self.load_guide(target,view=True)
            elif action=="system":
                resource=target
            else:
                resource=False
            return action,resource
        except (ValueError, IndexError, UnboundLocalError):
            return None,False
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
        target=target.split()
        engine,search_query=target[0]," ".join(target[1:])
        print(f"Searching for {search_query} using {engine} engine...")
        url=self.url.generate_query(engine,search_query)
        return url
    def create_guide(self,target,workspace_resources):
        workspace_name=self.workspace_name(target)
        resources=[]
        types=[]
        browser=[]
        for data in workspace_resources:
            resources.append(data[0])
            types.append(data[1])
            browser.append(data[2])
        self.paths.store_data(workspace_name,resources,resource_type=types,type="workspace",browsers=browser)
    def load_guide(self,target,view=False):
        workspace=self.workspace_name(target)
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

    def workspace_name(self,target):
        parts=target.split()
        if len(parts)>1 and parts[0].lower() in ("workspace","project"):
            return " ".join(parts[1:])
        return target.strip()




