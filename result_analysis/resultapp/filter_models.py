class TotalStudentResult(object):
    def __init__(self, s_pass, s_fail, total):
        self.total = total
        self.s_pass = s_pass
        self.s_fail = s_fail
        self.percentage = self.s_pass * 100 / self.total

class GenderWiseResult(object):
    def __init__(self, girls, boys, total):
        self.girls_result = TotalStudentResult(girls.s_pass, girls.s_fail, girls.total)
        self.boys_result = TotalStudentResult(boys.s_pass, boys.s_fail, boys.total)
        self.total = total

class BranchWiseResult(object):
	def __init__(self, name, code, total, s_pass, s_fail):
		self.name = name
		self.code = code
        self.total = total
        self.all_result = TotalStudentResult(s_pass.all, s_fail.all, self.total)
        self.gender_result = GenderWiseResult(s_pass.girls, s_fail.boys, self.total)


