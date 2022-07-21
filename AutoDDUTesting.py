from AutoDDU_CLI import mainpain
# For testing you pass in a list with
# [{'NVIDIA GeForce RTX 3080': ['GA102', '10de', '2206']}, []]
#                   GPU infos                           , 


List_of_tests = [
    [{'GeForce RTX 3080': ['GA102', '10de', '2206']}, []],
    [{'GeForce GT 630': ['GF108', '10de', '0f00']},[]], # https://github.com/Evernow/AutoDDU_CLI/issues/18
    [{'NVIDIA GeForce GTX 690': ['GK104', '10de', '1188'], 'Intel(R) UHD Graphics 630': ['CoffeeLake-S', '8086', '3e92']}, []], # Thank you Reki 
    [{'Intel(R) UHD Graphics 620': ['UHD', '8086', '5917']},[]]
]

for test in List_of_tests:
    try:
        print(mainpain(test))
    except:
        raise Exception("I am at the end of my rope")