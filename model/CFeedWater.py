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
        yfh_in = inlets[0].exergy_f(t0, p0)
        yfh_out = outlets[0].exergy_f(t0, p0)
        yfc_in = inlets[1].exergy_f(t0, p0)
        yfc_out = outlets[1].exergy_f(t0, p0)
        m_h = m_in[0]
        m_c = m_in[1]
        a = m_c*(yfc_out-yfc_in)
        b = m_h*(yfh_in-yfh_out)
        self.ef = b/a
        self.w = 0