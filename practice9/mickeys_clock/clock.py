import datetime

def angles():
    now = datetime.datetime.now()
    m = now.minute
    s = now.second

    m_angle = m * 6
    s_angle = s * 6

    return m_angle, s_angle