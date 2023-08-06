from typing import Iterable
from enum import IntEnum
import numpy as np
from ..framework.Edit import Allele, Edit
from ..utils.arithmetric import jaccard

AA_SET = {'A', 'C', 'D', 'E', 'F', 
'G', 'H', 'I', 'K', 'L', 
'M', 'N', 'P', 'Q', 'R',
 'S', 'T', 'V', 'W', 'Y', '*', '/'}


class MutationType(IntEnum):
    NO_CHANGE = -1
    SYNONYMOUS = 0
    MISSENSE = 1
    NONSENSE = 2

class AminoAcidEdit(Edit):
    def __init__(self, pos: int, ref: str, alt: str):
        self.pos = int(pos)
        assert ref in AA_SET, "Invalid ref aa: {}".format(ref)
        assert alt in AA_SET, "Invalid alt aa: {}".format(alt)
        self.ref = ref
        self.alt = alt

    @classmethod
    def from_str(cls, edit_str):
        pos, aa_change = edit_str.split(":")
        ref, alt = aa_change.split(">")
        return(cls(pos, ref, alt))

    def get_abs_edit(self):
        return("A"+self.__repr__())

    def __repr__(self):
        return("{}:{}>{}".format(int(self.pos),
        self.ref, self.alt))

    def __hash__(self):
        return(hash(self.__repr__()))

    def _severity(self):
        if self.ref == self.alt: return(MutationType.SYNONYMOUS)
        if self.alt == "*": return(MutationType.NONSENSE)
        if self.alt in AA_SET: return(MutationType.MISSENSE)
        else:
            raise ValueError("Alt base invalid:{}".format(self.alt))

    def __eq__(self, other):
        if (
            self.pos == other.pos
            and self.ref == other.ref
            and self.alt == other.alt
        ):
            return True
        return False

    def __lt__(self, other): # Implemented for pandas compatibility
        return self.pos < other.pos

    def __gt__(self, other): # Implemented for pandas compatibility
        return self.pos > other.pos

class AminoAcidAllele(Allele):
    def __init__(self, edits: Iterable[AminoAcidEdit] = None):
        if edits is None:
            self.edits = set()
        else:
            self.edits = set(edits)

    @classmethod
    def from_str(cls, allele_str): #pos:strand:start>end
        if type(allele_str) is AminoAcidAllele: return(allele_str)
        edits = set()
        try:
            for edit_str in allele_str.split(","):
                edit = AminoAcidEdit.from_str(edit_str)
                edits.add(edit)
        except ValueError:
            if allele_str.strip() == '':
                return(cls(None))
        return(cls(edits))

    def get_most_severe(self):
        if len(self.edits) == 0:
            return(MutationType.NO_CHANGE)
        severities = []
        for edit in self.edits:
            severities.append(edit._severity())
        return(max(severities))


class CodingNoncodingAllele():
    def __init__(self, aa_edits: Iterable[AminoAcidEdit] = None, base_edits: Iterable[Edit] = None, unique_identifier = None):
        self.aa_allele = AminoAcidAllele(aa_edits)
        self.nt_allele = Allele(base_edits)
        self.uid = unique_identifier
        if not self.uid is None:
            self.set_uid(self.uid)

    @classmethod
    def from_str(cls, allele_str):
        if isinstance(allele_str, cls): return(allele_str)
        uid = None
        if '!' in allele_str:
            uid, allele_str = allele_str.split('!')
        try:
            aa_allele_str, nt_allele_str = allele_str.split("|")
            aa_allele = AminoAcidAllele.from_str(aa_allele_str)
            nt_allele = Allele.from_str(nt_allele_str)
        except ValueError:
            if allele_str.strip() == '':
                return(cls(None))
            else:
                print(allele_str)
        return(cls(aa_allele.edits, nt_allele.edits, unique_identifier = uid))

    @classmethod
    def match_str(cls, allele_str):
        try:
            aa_allele, nt_allele = allele_str.split("|")
            aa_match = AminoAcidAllele.match_str(aa_allele)
            nt_match = Allele.match_str(nt_allele)
            return(aa_match and nt_match)
        except:
            return False 

    def get_most_severe(self):
        aa_sev = self.aa_allele.get_most_severe()
        if len(self.nt_allele.edits) > 0: return max(aa_sev, 0.1)
        return aa_sev

    def set_uid(self, uid):
        self.uid = uid
        self.nt_allele.edits = set([e.set_uid(uid) for e in self.nt_allele.edits])

    def get_jaccard(self, other):
        aa_jaccard = jaccard(self.aa_allele.edits, other.aa_allele.edits)
        nt_jaccard = jaccard(self.nt_allele.edits, other.nt_allele.edits)
        return(aa_jaccard, nt_jaccard)

    def map_to_closest(self, allele_list, aa_jaccard_threshold = 0.5, nt_jaccard_threshold = 0.5, merge_priority: np.ndarray = None):
        '''
        Arguments
        merge_priority -- Priority on which allele to merge if the jaccard index is the same.
        '''
        if len(allele_list) == 0: return(Allele())
        aa_jaccards, nt_jaccards = zip(*list(map(lambda o: self.get_jaccard(o), allele_list)))
        if not np.isnan(np.nanmax(aa_jaccards)):
            aa_max_idx = np.where(aa_jaccards == np.nanmax(aa_jaccards))[0]
            if len(aa_max_idx) > 1:
                nt_max_idx = np.where(nt_jaccards[aa_max_idx] == np.nanmax(nt_jaccards[aa_max_idx]))[0]
                if len(nt_max_idx) > 1 and not merge_priority is None:
                    if not len(merge_priority) == len(allele_list):
                        raise ValueError("merge_priority length {} is not the same as allele_list length {}".format(len(merge_priority), len(allele_list)))
                    nt_max_idx = nt_max_idx[np.argmax(merge_priority[nt_max_idx])]
                else:
                    nt_max_idx = nt_max_idx[0]
                both_max_idx = aa_max_idx[nt_max_idx]
                if aa_jaccards[both_max_idx] > aa_jaccard_threshold and nt_jaccards[both_max_idx] > nt_jaccard_threshold:
                    return(allele_list[nt_max_idx.item()])
        return(Allele())

    def __repr__(self):
        if not self.uid is None:
            return self.uid + "!" + str(self.aa_allele) + "|" + str(self.nt_allele)
        return str(self.aa_allele) + "|" + str(self.nt_allele)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return False
        return(self.uid == other.uid and self.aa_allele == other.aa_allele and self.nt_allele == other.nt_allele)
    
    def __lt__(self, other):
        if self.aa_allele < other.aa_allele: return True
        if self.aa_allele == other.aa_allele:
            if self.nt_allele < other.nt_allele: return True
        return False

    def __gt__(self, other):
        if self.aa_allele > other.aa_allele: return True
        if self.aa_allele == other.aa_allele:
            if self.nt_allele > other.nt_allele: return True
        return False

    def __hash__(self):
        return(hash(self.__repr__()))


