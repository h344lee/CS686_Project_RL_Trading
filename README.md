## What is this?

It is a Deep Q learning based US stock trading algorithm.

- The performance of this algorithm is compared to the buy-and-hold strategy.
<img src="https://github.com/h344lee/CS686_Project_RL_Trading/blob/master/GOOGL_buy_and_hold.png" width="300" height="200">

- It can present different performance based on the LSTM value network step size.
<img src="https://github.com/h344lee/CS686_Project_RL_Trading/blob/master/GOOGL_present_steps.png" width="300" height="200">

## Environment
- [Anaconda 3.7+](https://www.anaconda.com/distribution/)
- [TensorFlow 1.15.2](https://www.tensorflow.org/)
  - `pip install tensorflow==1.15.2`
- [plaidML](https://plaidml.github.io/plaidml/)
  - `pip install plaidml-keras==0.6.2`
  - `pip install mplfinance`
  
## How to run? 

You can run this program in Google Colab pretty easily


```markdown
!pip uninstall -y tensorflow
!pip install tensorflow-gpu==1.15
!pip install mplfinance
!pip install yfinance
!git clone https://github.com/h344lee/CS686_Project_RL_Trading.git
```

```markdown
%cd /content/CS686_Project_RL_Trading
!python ./main.py   
``` 
 
 
## Declaimer 
The source code can be changed in anytime. 
 
 
## It is based on the Quantylab open source project 

URL : https://github.com/quantylab/rltrader.git


