from harmony_model_checker.harmony.ops import *

class Labeled_Op:
    def __init__(self, op, start, stop, stmt, labels):
        self.op = op
        self.start = start
        self.stop = stop
        self.stmt = stmt
        self.labels = labels
        self.live_in = set()
        self.live_out = set()

class Code:
    def __init__(self):
        self.labeled_ops = []
        self.endlabels = set()
        self.curFile = None
        self.curLine = 0

    def location(self, file, line):
        self.curFile = file
        self.curLine = line

    def append(self, op, start, stop, labels=set(), stmt=None):
        assert len(start) == 4
        assert len(stop) == 4
        self.labeled_ops.append(Labeled_Op(op, start, stop, stmt, labels | self.endlabels))
        self.endlabels = set()

    def nextLabel(self, endlabel):
        self.endlabels.add(endlabel)

    def delete(self, var):
        assert False        # TODO: I think this code is obsolete

    # This method inserts DelVar operations as soon as a variable is no
    # longer live
    def liveness(self):
        # First figure out what the labels point to and initialize
        # the nodes
        map = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            lop.pred = set()
            lop.live_in = set()
            lop.live_out = set()
            for label in lop.labels:
                assert label not in map, label
                map[label] = pc
        # Compute the predecessors of each node
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            if isinstance(lop.op, JumpOp):
                assert isinstance(lop.op.pc, LabelValue)
                succ = self.labeled_ops[map[lop.op.pc]]
                succ.pred |= {pc}
            elif isinstance(lop.op, JumpCondOp):
                assert pc < len(self.labeled_ops) - 1
                assert isinstance(lop.op.pc, LabelValue)
                succ = self.labeled_ops[map[lop.op.pc]]
                succ.pred |= {pc}
                self.labeled_ops[pc + 1].pred |= {pc}
            elif pc < len(self.labeled_ops) - 1 and not isinstance(lop.op, ReturnOp):
                self.labeled_ops[pc + 1].pred |= {pc}
        # Live variable analysis
        change = True
        while change:
            change = False
            for pc in range(len(self.labeled_ops)):
                lop = self.labeled_ops[pc]
                if pc == len(self.labeled_ops) - 1:
                    live_out = set()
                elif isinstance(lop.op, JumpOp):
                    assert isinstance(lop.op.pc, LabelValue)
                    succ = self.labeled_ops[map[lop.op.pc]]
                    live_out = succ.live_in
                else:
                    live_out = self.labeled_ops[pc + 1].live_in
                    if isinstance(lop.op, JumpCondOp):
                        assert isinstance(lop.op.pc, LabelValue)
                        succ = self.labeled_ops[map[lop.op.pc]]
                        live_out = live_out | succ.live_in
                live_in = lop.op.use() | (live_out - lop.op.define())
                if not change and (live_in != lop.live_in or live_out != lop.live_out):
                    change = True
                lop.live_in = live_in
                lop.live_out = live_out
        # Create new code with DelVars inserted
        newcode = Code()
        for lop in self.labeled_ops:
            # print(lop.op, lop.live_in, lop.live_out)
            (_, file, line, _)  = lop.start

            # If a variable is live on output of any predecessor but not
            # live on input, delete it first
            lop.pre_del = set()
            for pred in lop.pred:
                plop = self.labeled_ops[pred]
                live_out = plop.live_out | plop.op.define()
                lop.pre_del |= live_out - lop.live_in

            labels = lop.labels
            for d in sorted(lop.pre_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), lop.start, lop.stop, labels=labels, stmt=lop.stmt)
                labels = set()
            newcode.append(lop.op, lop.start, lop.stop, labels=labels, stmt=lop.stmt)

            # If a variable is defined or live on input but not live on output,
            # immediately delete afterward
            # TODO.  Can optimize StoreVar by replacing it with Pop
            # lop.post_del = (lop.op.define() | lop.live_in) - lop.live_out
            lop.post_del = lop.live_in - lop.live_out
            for d in sorted(lop.post_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), lop.start, lop.stop, stmt=lop.stmt)

        return newcode

    def link(self):
        map = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            for label in lop.labels:
                assert label not in map, label
                map[label] = PcValue(pc)
        for lop in self.labeled_ops:
            lop.op.substitute(map)

