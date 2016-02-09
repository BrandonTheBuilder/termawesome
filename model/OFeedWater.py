class OFeedWater(object):
    """docstring for FeedWater"""
    def __init__(self, inlets, m_in, outlet, m_out, t0, p0):
        self.entropyProduced = (
            sum([inlets[i].properties['s']*m_in[i] for i in range(len(inlets))])
            -outlet.properties['s']*m_out[0])

        self.exergyDestroyed = self.entropyProduced*t0
        self.yf_in = sum([inlets[i].exergy_f(t0, p0)*m_in[i] for i in range(len(m_in))])
        self.yf_out = outlet.exergy_f(t0, p0)*m_out[0]
        yfo = outlet.exergy_f(t0, p0)
        yfh = inlets[0].exergy_f(t0, p0)
        yfc = inlets[1].exergy_f(t0, p0)
        c = m_in[0]*(yfo - yfc)
        h = m_in[1]*(yfh-yfo)
        self.ef = c/h
        self.w = 0