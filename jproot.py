import ROOT

def lsroot(infile):
    if not type(infile) == ROOT.TFile:
        infile = ROOT.TFile(infile)

    key_list = infile.GetListOfKeys()

    for one_key in key_list:
        print 'Key:', one_key.GetName()
        
        branches = infile.Get(one_key).GetListOfBranches()
        for one_branch in branches:
            print '\tBranch:', one_branch.GetName()

            branches2 = infile.Get(one_key).GetBranch(one_branch).GetListOfBranches()
            for one_branch2 in branches2:
                print '\t\tBranch2:', one_branch2.GetName()

            leaves = infile.Get(one_key).GetBranch(one_branch).GetListOfLeaves()
            for one_leaf in leaves:
                print '\t\tLeaf', one_leaf.GetName()

            baskets = infile.Get(one_key).GetBranch(one_branch).GetListOfBaskets()
            for one_basket in baskets:
                print '\t\tBaskets:', one_basket.GetName()
