if __name__ == "__main__":
    from system_crash_bn import *
    
    # get system crash bn
    sc_bn = generate_bn()
    
    # visualize the model to confirm structure
    viz = sc_bn.to_graphviz()
    viz.draw('sc_bn.png', prog='dot');
    del viz
    
    # do some exact inference
    queries = {'P(C)' : exact_inference(sc_bn, variables=['C'], evidence=None),
               'P(H | -s, -c)' : exact_inference(sc_bn, variables=['H'], evidence={'S': False, 'C': False}),
               'P(W | c)' : exact_inference(sc_bn, variables=['W'], evidence={'C': True}),
               'P(C | -s, h)' : exact_inference(sc_bn, variables=['C'], evidence={'S': False, 'H': True}),
               'P(S, C | -m)' : exact_inference(sc_bn, variables=['S', 'C'], evidence={'M': False})
               }
    
    for q in queries:
        print(f'{q} = {queries[q]}')