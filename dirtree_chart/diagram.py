import os
from .utils import helpers


class DirStrucTree:

    '''
    A class to create a directory structure diagram with the help of mermaid.
    
    Parameters
    ----------
    root : string
        The root path where the structure tree should start. Default is '.'.
    ignore : list
        A list with folders to ignore.
    files : boolean
        If files should be included in the structure diagram.
    style : array
        An array with style lines elements. 
        default = [
            "classDef root fill:#fff, stroke-width:0px;",
            "classDef folder fill:#f7ce7f, stroke-width:0px;",
            "classDef file fill:#f2f2f2, stroke-width:0px;"
        ]
        
    Attributes
    ----------
    root : string
        See above
    ignorre : string
        See above
    layerHierarchy : dict
        The folders layer hierarchy
    layerHierarchyWithIds : dict
        The layer hierarchy with ids used for the connections.
    output_format : string
        TODO
    include_to_readme : boolean
        If the mermaid diagram should be included in a README file. 
    direction : string
        The direction of the tree diagram. Possible values: 'LR', 'RL', 'TD'.
        Default: 'LR'.
    '''    

    def __init__(self,
                 root=os.getcwd(), 
                 ignore=[], 
                 files = False, 
                 style = None,
                 output_format = 'raw',
                 include_to_readme = False,
                 direction = "LR",
                 max_folder_depth = 4):

        self.root = root
        self.ignore = set(ignore)
        self.layerHierarchy = {}
        self.layerHierarchyWithIds = None
        self.files = files
        self.include_to_readme = include_to_readme
        self.oFp = None
        self.maxFolderDepth = max_folder_depth
        self.direction = direction 
        
        if style is None:
            self.style = self.getDefaultStyle()
        else:
            style = style

        self._createLayerHierarchy()
        self.generateFile()
        

    def generateFile(self):
        
        '''
        Generates the output file.
        '''
        
        gen = FileGenerator(self)
        gen.buildFileBlocks()
        gen.setStyle(self.style)
        
        self.oFp = os.path.join(self.root, "dirstruc_diagram.mmd")
        
        gen.writeBlocksToFile(self.oFp)
        
        if self.include_to_readme is True:
            gen.includeToReadme()


    def getDefaultStyle(self):
        
        '''
        Mermaids default style.
        
        Returns
        -------
        Array
            Each style lines as an array element.
        '''
        
        lines = [
            "classDef root fill:#fff, stroke-width:0px;",
            "classDef folder fill:#f7ce7f, stroke-width:0px;",
            "classDef file fill:#f2f2f2, stroke-width:0px;"
        ]

        return lines


    def _addLayerToHierarchy(self, layer):

        '''
        Adds a layer to the folder levels hierarchy.
        
        Parameters
        ----------
        layer : list
            A list with the current folder where the length of this
            list is the current level. A list with length 1 is a folder of
            the current root path. A list with length 2 is a subfolder of this
            root folder.
        '''        

        level = len(layer)
        
        if level not in self.layerHierarchy:
            self.layerHierarchy[level] = []
        
        if level <= self.maxFolderDepth:
            self.layerHierarchy[level].append(layer)


    def _addIdsToLayerHierarchy(self):

        '''
        Main algorithm to assign each folder and file a mermaid conform ID.
        The result is a hierachically layerd dict.
        '''  
        
        self.layerHierarchyWithIds = self.layerHierarchy.copy() 
        
        for levelId, levelGroup in self.layerHierarchyWithIds.items():

            newLayerFolders = {}
            layerFolderGroupCounter = 1
            fromIdBefore = -1
         
            for layerFolderGroup in levelGroup:

                layerFolderCounter = 1 
                for folder in layerFolderGroup:
 
                    # Do this for the last element in the layerFolderGroup (this is the splitted relative path) 
                    if len(layerFolderGroup) == layerFolderCounter:

                        if levelId > 1:
                            pos = layerFolderCounter-1
                            fromId = self.layerHierarchyWithIds[pos][layerFolderGroup[pos-1]]["id"]
                            
                            if fromIdBefore != fromId:
                                layerFolderGroupCounter = 1
                            
                            val = "{}.{}".format(
                                fromId, layerFolderGroupCounter)
                            
                            fromIdBefore = fromId
                        else:
                            val = layerFolderGroupCounter
                        
                        typ = "d"
                        fnSplitted = folder.split(".")
                        if len(fnSplitted) > 1: # files
                            typ = "f"
                            if folder in newLayerFolders.keys():
                                # Add this trailing info if file (key) already exists on this level
                                folder = "{}__mermaid__{}".format(folder, fromId)
                            newLayerFolders[folder] = {
                                "id": val,
                                "type": typ,
                                "ext": fnSplitted[-1]
                            }
                        else: # folders
                            if folder in newLayerFolders.keys():
                                folder = "{}__mermaid__{}".format(folder, fromId)
                            newLayerFolders[folder] = {
                                "id": val,
                                "type": typ
                            }

                    layerFolderCounter = layerFolderCounter + 1

                layerFolderGroupCounter = layerFolderGroupCounter + 1

            self.layerHierarchyWithIds[levelId] = newLayerFolders


    def _createLayerHierarchy(self):
        
        '''
        Creation of the whole level hierarchy
        '''
        
        self._tree_walker(self.ignore)
        self._addIdsToLayerHierarchy()


    def _pathWithoutRoot(self, root, d):
        
        '''
        Create a path to the current root dir without the main root (self.root). 
        root != self.root
        
        Parameters
        ----------
        root : path
            The current root path
        
        d : string
            The current file or dir of that root
        
        Returns
        -------
        path
            The current path to the folder or file without the main root.    
        '''
        
        dirPath = os.path.normpath(os.path.join(root, d))
        rootPathLen = len(helpers.splitall(self.root))
        dirPathNoRoot = helpers.splitall(dirPath)[rootPathLen:]
        
        return dirPathNoRoot


    def _tree_walker(self, ignore=[]):

        '''
        Walks to the root folder and adds the folder as layers to the 
        layerHierarchy.
        
        Parameters
        ----------
        ignore : list
            The folders to ingore.
        
        '''        

        for root, dirs, files in os.walk(self.root, topdown=True):
            dirs[:] = [d for d in dirs if d not in ignore]

            for d in dirs:
                path = self._pathWithoutRoot(root, d)
                self._addLayerToHierarchy(path)
    
            for f in files:
                if f not in ignore:
                    path = self._pathWithoutRoot(root, f)
                    self._addLayerToHierarchy(path)



class FileGenerator:
    
    '''
    Class to build up the file with the layerHierarchy as input. 
    
    Parameters
    ----------
    
    
    '''
    
    def __init__(self, mermaid):
        
        self.mermaid = mermaid
        self.layerHierarchy = mermaid.layerHierarchyWithIds
        self.root = mermaid.root
        self.rootBlock = []
        self.mainBlock = []
        self.parentDirIdCounter = None
        self.idFromBefore = None
        self.style = None


    def buildRootLines(self, items):

        '''
        Build the root lines. This is necessary because of the different 
        syntax handling.
        
        Parameters
        ----------
        items : dict_items
            The folder or files with its props (id, type, extension ...)
            
        Returns
        -------
        Array 
            The lines as an array
        '''
        
        lines = []
        for name, props in items:
                lines.append(self.buildRootLine(props["id"], props["type"],  name))
        
        return lines


    def buildHeader(self):
        header = ["graph {}".format(self.mermaid.direction)]

        return header


    def buildRootLine(self, id, type, name):
        
        if type == "d":
            line = "\troot[{}]:::root --> {}({}):::folder".format(os.path.split(self.root)[1], id, name)
        else:
            line = "\troot[{}]:::root --> {}[{}]:::file".format(os.path.split(self.root)[1], id, name)
        
        return line

    
    def buildMainLines(self, items):

        '''
        The core algorithm for for building the structure with all the 
        connections and of files and folders. This method gets calles for
        each level.
        
        Parameters
        ----------
        items : dict_items
            The folder or files with its props (id, type, extension ...)
        
        Returns
        -------
        Array
            An array with all the lines to write
        '''
        
        def buildLinesForFilenames(filenames, lines, id):
            
            filesnamesString = str(filenames).replace("'", "").replace(", ", "<br>")
            line = "\t{} --> {}{}:::file".format(self.idFromBefore, id, filesnamesString)  
            lines.append(line)
            filenames = [] 
            
            return filenames, lines
        
        lines = []
        filenames = []
        idBefore = None
        
        if len(items) == 0:
            return lines
        
        for name, props in items:
            
            id = props["id"]
            
            idFrom = id.rsplit('.', 1)[0]
            
            # Remove trailing __mermaid__ for duplicated files and dirs for the level
            idf = '__mermaid__'
            if idf in name:
                name = name.split(idf)[0]
            
            if props["type"] == 'd':
                line = "\t{} --> {}({}):::folder".format(idFrom, id, name)
                lines.append(line)
            else:
                    
                if self.idFromBefore != idFrom and self.idFromBefore is not None and filenames:
                    filenames, lines = buildLinesForFilenames(filenames, lines, idBefore)
                    
                filenames.append(name)

                self.idFromBefore = idFrom
                idBefore = id
        
        # Add the last element 
        if props["type"] == 'f':
            filenames, lines = buildLinesForFilenames(filenames, lines, idBefore)      
        
        return lines


    def buildFileBlocks(self):

        '''
        Builds all the file blocks. The blocks are seperated into head, root
        main, style ... blocks.
        '''
        
        self.headerBlock = self.buildHeader()
        
        for level, val in self.layerHierarchy.items():
            
            items = val.items()
            
            if level == 1:
                self.rootBlock = self.buildRootLines(items)
            else:
                if not self.mainBlock:
                    self.mainBlock = self.buildMainLines(items)
                else:
                    self.mainBlock.extend(self.buildMainLines(items))
                               
     
    def setStyle(self, style):
        self.style = style
                
     
    def writeBlocksToFile(self, oFp):
        
        '''
        Writes all the blocks to a file 
        
        Parameters
        ----------
        oFp : path
            The path where to create the mermaid file.
        
        '''
        
        self.outfile = open(oFp, "w")
        
        self.outfile.write("\n".join(map(str, self.headerBlock)))
        self.outfile.write("\n")
        self.outfile.write("\n".join(map(str, self.rootBlock)))
        self.outfile.write("\n")
        self.outfile.write("\n".join(map(str, self.mainBlock)))
        self.outfile.write("\n")
        self.outfile.write("\n".join(map(str, self.style)))
        
        self.outfile.close()
        
        print("Saved file to: {}".format(oFp))
        
 
    def includeToReadme(self):

        '''
        Includes the mermaid chart to a README.md. TODO: Do this now only for
        .md files. If a mermaid chart already exists it will be overwritten. 
        '''        

        mermaidFileContent = ""
        start_pattern = '<!--  mermaid_start -->'
        end_pattern = '<!--  mermaid_end -->'
        
        with open(self.mermaid.oFp, "r") as file:
            mermaidFileContent = file.read()
           
        rmPath = "{}/README.md".format(self.root)
        
        if os.path.exists(rmPath):
            
            with open(rmPath, "r") as readme:
                readmeContent = readme.read()
                
            if '```mermaid' not in readmeContent:
                with open(rmPath, "a") as readme:
                    readme.write("\n\nProject Structure\n=================\n{sp}\n```mermaid\n{c}\n```\n{ep}".format(
                        c=mermaidFileContent,
                        sp=start_pattern,
                        ep=end_pattern))
            else:
                
                with open(rmPath) as file:
                    readBefore = True
                    readAfter = False
                    readmeContentCleanedBefore = ""
                    readmeContentCleanedAfter = ""
                    for line in file:
                      
 
                        if start_pattern in line:
                            readBefore = False
                        if end_pattern in line:
                            readAfter = True
                            
                        if readBefore:
                            readmeContentCleanedBefore += line

                        if readAfter and end_pattern not in line:
                            readmeContentCleanedAfter += line
                
                readmeContentCleanedWithChart = "{rcb}{sp}\n```mermaid\n{mcont}\n```\n{ep}\n{rca}".format(
                    rcb=readmeContentCleanedBefore,
                    mcont=mermaidFileContent,
                    rca=readmeContentCleanedAfter,
                    sp=start_pattern,
                    ep=end_pattern)

                with open(rmPath, "w") as readme:
                    readme.write(readmeContentCleanedWithChart)
                    
        else:
            print("Warning: Readme not found at '{}'".format(rmPath))
