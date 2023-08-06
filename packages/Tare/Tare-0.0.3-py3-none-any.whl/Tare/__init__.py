from .model.Model import Decoder
from .generation.Dataset import SumDataset
import pickle
import torch
import numpy as np
import os
import javalang
import traceback
class dotdict(dict):
    def __getattr__(self, name):
        return self[name]
args = dotdict({
    'NlLen':500,
    'CodeLen':60,
    'batch_size':96,
    'tbsize':4,
    'embedding_size':256,
    'WoLen':15,
    'Vocsize':100,
    'Nl_Vocsize':100,
    'max_step':3,
    'margin':0.5,
    'poolsize':50,
    'Code_Vocsize':100,
    'num_steps':50,
    'rulenum':10,
    'cnum':695,
    'use_apex':False,
    'mask_value':-1e9,
    'gradient_accumulation_steps':1,
    'max_grad_norm':5,
    'seed':19970316,
    'varlen':45,
    'mask_id':-1,
    'lookLoss':False,
    'patience':5,
    'max_num_trials':10
})
def gVar(data, use_cuda=False):
    tensor = data
    if isinstance(data, np.ndarray):
        tensor = torch.from_numpy(data)
    else:
        assert isinstance(tensor, torch.Tensor)
    if use_cuda:
        tensor = tensor.cuda()
    return tensor
def load_model(model, dirs = 'checkpointSearch/'):
    assert os.path.exists(dirs + 'best_model.ckpt'), 'Weights for saved model not found'
    model.load_state_dict(torch.load(dirs + 'best_model.ckpt'))
class Tare:
    def __init__(self, argUser=None, pathVoc="./", useCuda=True):
        super(Tare, self).__init__()
        if argUser is not None:
            self.args = argUser
        else:
            self.args = args
        self.pathVoc = pathVoc
        dev_set = SumDataset(args, "val", True, filepath=pathVoc)
        self.useCuda = useCuda
        rulead = gVar(pickle.load(open(pathVoc + "rulead.pkl", "rb")), self.useCuda).float().unsqueeze(0).repeat(2, 1, 1)
        self.args.cnum = rulead.size(1)
        self.args.Nl_Vocsize = len(dev_set.Nl_Voc)
        self.args.Code_Vocsize = len(dev_set.Code_Voc)
        self.args.Vocsize = len(dev_set.Char_Voc)
        args.rulenum = len(dev_set.ruledict) + args.NlLen
        self.model = Decoder(self.args)
        if self.useCuda:
            print('using GPU')
            self.model = self.model.cuda()
        self.model = self.model.eval()
    def loadModel(self, path2Model='./'):
        load_model(self.model, path2Model)
    def testDefect4j(self, bugid, locnum, pathloc, pathcontext):
        from .generation.testDefect4j import testDefect4j
        testDefect4j(bugid, pathloc, locnum, pathcontext, self.model, self.pathVoc, useCuda=self.useCuda)
    def predictOneMethod(self, method, location, beamsize=50):
        data = []
        try:
            lines1 = method
            liness = lines1.splitlines()
            tokens = javalang.tokenizer.tokenize(lines1)
            parser = javalang.parser.Parser(tokens)
            try:
                tree = parser.parse()
            except javalang.parser.JavaSyntaxError:
                tree = parser.parse_member_declaration()
            from .generation.testDefect4j import generateAST,getNodeById,getSubroot,getLineNode,getroottree,containID,setProb,turnold2new,getNodeNo,addter,getroottree_with_type,setProbwithPre,getById,setSameid,solveLongTree
            tmproot = getroottree(generateAST(tree))
            lineid = location
            currroot = getNodeById(tmproot, lineid)
            lnode, mnode = getSubroot(currroot)
            if mnode is None:
                print('cannot find the method node')
                return
            oldcode = liness[lineid - 1]
            subroot = lnode
            treeroot = mnode
            presubroot = None
            aftersubroot = None
            linenodes = getLineNode(treeroot, "")
            if subroot not in linenodes:
                print('cannot find the line node')
                return
            currid = linenodes.index(subroot)
            if currid > 0:
                presubroot = linenodes[currid - 1]
            if currid < len(linenodes) - 1:
                aftersubroot = linenodes[currid + 1]
            setProb(treeroot, 2)
            if subroot is None:
                print('cannot find the line node')
                return
            if True:
                cid = set(containID(subroot))
                subrootsave = subroot
                setProb(treeroot, 2)
                if subroot is not None:
                    setProb(subroot, 1)
                if aftersubroot is not None:
                    setProb(aftersubroot, 4)
                if presubroot is not None:
                    setProb(presubroot, 3)
                curridx = 0
                curridx, _ = getNodeNo(treeroot, subroot, 0)
                #print(curridx)
                subidx = curridx
                prob = subroot.getTreeProb(treeroot)
                newTree = turnold2new(subroot.printTree(treeroot).split())
                for pj in range(len(newTree) - 1):
                    if newTree[pj + 1] == '^' and newTree[pj] != '^':
                        newTree[pj] = newTree[pj] + '_ter'
                addter(subrootsave)
                treeroot = getroottree_with_type(newTree)
                setProbwithPre(treeroot, prob)
                subroot = getById(treeroot, subidx)
                #print(subroot.printTree(subroot))
                linenodes = getLineNode(treeroot, "")
                idx = linenodes.index(subroot)
                if idx + 1 < len(linenodes):
                    curridm = linenodes[idx + 1]
                else:
                    curridm = None
                maxl = -1
                minl = 1e10
                for l in cid:
                    maxl = max(maxl, l - 1)
                    minl = min(minl, l - 1)
                precode = "\n".join(liness[0:minl])
                aftercode = (maxl + 1, len(liness))
                oldcode = "\n".join(liness[minl:maxl + 1])
                troot, vardic, typedic, varwithts = solveLongTree(treeroot, subroot, curridm)
                setSameid(subroot, subrootsave)
                data.append({'treeroot': treeroot, 'troot': troot, 'oldcode': oldcode, 'subroot': subrootsave, 'vardic': vardic, 'typedic': typedic,'precode': precode, 'aftercode': aftercode, 'tree': troot.printTreeWithVar(troot, vardic), 'prob': troot.getTreeProb(troot), 'mode': 0, 'line': lineid, 'isa': False, 'varwithtype':varwithts, 'extended':False, 'idss':'test','classname':'test'})
                #print(data)
                from .generation.run import solveone
                ans = solveone(data, self.model, self.pathVoc, beamsize)
                return ans
        except:
            traceback.print_exc()
            return None