d = {1:5,2:7,3:9,5:8,9:10}
sd = sorted(d.items(), key=lambda kv: kv[1],reverse=True)
print(sd)
print(sd[:2])
print(list(sd))
print(sd[:2])