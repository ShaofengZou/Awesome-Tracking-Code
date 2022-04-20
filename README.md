# AwesomeTrackingCode
python code implement of awesome tracking algorithms

## Code Reference
1. MOSSE [github](https://github.com/TianhongDai/mosse-object-tracking)
2. CSK [github](https://github.com/hsjeong5/CSK)
3. KCF [github](https://github.com/chuanqi305/KCF)
 got error when roi exceeding the image
4. KCF [github](https://github.com/LCorleone/KCF_py3)
## Run Example
1. MOSSE
> python 01-MOSSE\demo.py
2. CSK
> python 02-CSK\demo.py
3. KCF
> python 04-KCF\run.py datasets\surfer
## Effect Compare
1. 对于surf数据集，框住全身，MOSSE、CSK都可以跟住目标
2. 对于surf数据集，框住头部，MOSSE算法会更丢目标，CSK算法可以跟住目标
3. 对于M1数据，CSK算法在中间会丢失目标