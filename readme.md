# CDRetainer
(A ProxyPool Retainer on Python)   
- You set several urls.
- then **CDRetainer** will crawl free proxylist from network *automatically*.
- After filter function, make a proxylist for each target.

-------------------

### Usage    

```python
git clone https://github.com/okcd00/CDRetainer.git
cd CDRetainer
vim sourcelist.txt # Change conf by yourself, default 3 targets
vim conf/Basic.conf # Change paras by yourself, default run once per 43200 seconds
nohup python CDRetainer.py &
# Then get Result in `./data`
```

### Dependency
+ [Python](http://www.python.org/)
+ urllib2
+ ConfigParser

### New Idea
- [x] Make a `Configure` out of Source Code
- [x] Custom `Sourcelist` for different aims

### UpdateLog    
[2015/11/10] ver 1.0.0
+ Add `Basic.conf` Config Function
+ Demo with `Logger` Complete
