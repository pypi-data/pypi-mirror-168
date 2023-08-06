import numpy as np

def unpack_float_acphy(nbits: int, autoscale: int, shft: int, fmt: int, nman: int, nexp: int, nfft: int,
                       H: np.array) -> np.array:
    k_tof_unpack_sgn_mask = (1 << 31)

    He = [0] * nfft
    Hout = [0] * nfft*2

    iq_mask = (1 << (nman - 1)) - 1
    e_mask = (1 << nexp) - 1
    e_p = (1 << (nexp - 1))
    sgnr_mask = (1 << (nexp + 2 * nman - 1))
    sgni_mask = (sgnr_mask >> nman)
    e_zero = -nman

    # print('e_p', e_p)

    out = np.zeros((nfft * 2), dtype=np.int64)
    n_out = (nfft << 1)
    e_shift = 1
    maxbit = -e_p

    # print(bin(iq_mask), bin(e_mask))
    # print(bin(sgnr_mask), bin(sgni_mask))

    for i in range(len(H)):
        vi = ((H[i] >> (nexp + nman)) & iq_mask)
        vq = ((H[i] >> nexp) & iq_mask)
        e = (H[i] & e_mask)

        # print(i, ':', vi, vq, e)
        # print(i, ':', e)

        if e >= e_p:
            e -= (e_p << 1)

        He[i] = e

        if H[i] & sgnr_mask:
            vi |= k_tof_unpack_sgn_mask

        if H[i] & sgni_mask:
            vq |= k_tof_unpack_sgn_mask

        Hout[i << 1] = vi
        Hout[(i << 1) + 1] = vq

    shft = nbits - maxbit
    for i in range(n_out):
        e = He[(i >> e_shift)] + shft
        vi = Hout[i]

        sgn = 1

        if vi & k_tof_unpack_sgn_mask:
            sgn = -1

            vi &= ~k_tof_unpack_sgn_mask

        if e < e_zero:
            vi = 0
        elif e < 0:
            e = -e
            vi = (vi >> e)
        else:
            vi = (vi << e)

        out[i] = sgn * vi

    for i in range(int(len(out) / 2)):
        o = [out[2*i], out[2*i + 1]]
        
        power = 0
        while o[0] % 2 == 0 and o[1] %2 == 0:
            if o[0] == 0 and o[1] == 0: break

            o[0] = o[0] / 2
            o[1] = o[1] / 2

            power += 1

        # print(i, ':', int(abs(o[0])), int(abs(o[1])), power)
        # print(i, ':', power - 10)
        print(i, ':', power, int(abs(o[0])), int(abs(o[1])))

    # for o in out:
    #     power = 0
    #     while o % 2 == 0:
    #         if o == 0: break
    #         o = o / 2
    #         power += 1
        
    #     print(o, power)

    return out
