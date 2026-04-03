from alignment import *


def main():
    str1 = "1 Hearken and hear this, O house of Jacob, who are called by the name of Israel, and are come forth out of the waters of Judah, or out of the waters of baptism, who swear by the name of the Lord, and make mention of the God of Israel, yet they swear not in truth nor in righteousness."
    str2 = "1 Hear ye this, O house of Jacob, which are called by the name of Israel, and are come forth out of the waters of Judah, which swear by the name of the Lord, and make mention of the God of Israel, but not in truth, nor in righteousness."

    alignunbounded = align(str1, str2, banded_width=-1)
    alignbounded = align(str1, str2, banded_width=48)
    localalign = local_align(str1, str2, match_award=-4, indel_penalty=3, sub_penalty=2)

    print(f"align unbounded: {alignunbounded}\n")
    print(f"align bounded: {alignbounded}\n")
    print(f"local align: {localalign}\n")

    print(f"unbounded count: {len(alignunbounded[1])}")
    print(f"bounded count: {len(alignbounded[1])}")
    print(f"similarities count: {len(localalign[1])}")




if __name__ == "__main__":
    main()