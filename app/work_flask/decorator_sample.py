"""
def a():
	print("Aです")


def b(func):
	print("=started=")
	func()
	print("=end=")


def outer(func):
	def inner():
		print("=started=")
		func()
		print("=end=")
	return inner
"""


def outer(func):
	def inner(*args, **kwargs):
		print("=started=")
		func(*args, **kwargs)
		print("=end=")
	return inner



nums=(10,20,30,40)

@outer
def show_sum(nums):
	res = sum(nums)
	print(res)
	return res


show_sum(nums)