class CFeedWater(object):
    """docstring for FeedWater"""
    def __init__(self, inlets, m_in, outlets, m_out, t0, p0):
        self.entropyProduced = (
            sum([inlets[i].properties['s']*m_in[i] for i in range(len(inlets))])
            -sum([outlets[i].properties['s']*m_out[i] for i in range(len(inlets))]))
        self.exergyDestroyed = self.entropyProduced*t0
        yf_in = [inlets[i].exergy_f(t0, p0)*m_in[i] for i in range(len(m_in))]
        self.yf_in = sum(yf_in)
        yf_out = [outlets[i].exergy_f(t0, p0)*m_out[i] for i in range(len(m_out))]
        self.yf_out = sum(yf_out)
        self.ef = (yf_out[1]-yf_in[1])/(yf_in[0]-yf_out[0])
        self.w = 0