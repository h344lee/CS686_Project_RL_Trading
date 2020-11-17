import os
import sys
import logging
import argparse
import json

import get_data
import settings
import utils
import data_manager
import visualizer


def init(stock_code, num_epoches, num_steps ):

    #--stock_code MSFT --rl_method dqn --net lstm --num_steps 5 --learning --num_epoches 10 --lr 0.001 --start_epsilon 1 --discount_factor 0.9

    parser = argparse.ArgumentParser()
    parser.add_argument('--stock_code', default=stock_code)
    parser.add_argument('--ver', choices=['v1', 'v2'], default='v1')
    parser.add_argument('--rl_method', default='dqn')
    parser.add_argument('--net', default='lstm')
    parser.add_argument('--num_steps', type=int, default=num_steps)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--discount_factor', type=float, default=0.9)
    parser.add_argument('--start_epsilon', type=float, default=1)
    parser.add_argument('--balance', type=int, default=100000)
    parser.add_argument('--num_epoches', type=int, default=num_epoches)
    parser.add_argument('--delayed_reward_threshold', type=float, default=0.05)
    parser.add_argument('--backend', choices=['tensorflow', 'plaidml'], default='tensorflow')
    parser.add_argument('--output_name', default=utils.get_time_str())
    parser.add_argument('--value_network_name')
    parser.add_argument('--policy_network_name')
    parser.add_argument('--reuse_models', action='store_true')
    parser.add_argument('--learning', default=True)
    parser.add_argument('--start_date', default='20160713')
    parser.add_argument('--end_date', default='20191231')
    args = parser.parse_args()

    return args

def executor(agrs) :
    # Keras Backend 설정
    if args.backend == 'tensorflow':
        os.environ['KERAS_BACKEND'] = 'tensorflow'
    elif args.backend == 'plaidml':
        os.environ['KERAS_BACKEND'] = 'plaidml.keras.backend'

    # 출력 경로 설정
    output_path = os.path.join(settings.BASE_DIR,
                               'output/{}_{}_{}'.format(args.output_name, args.rl_method, args.net))
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    # 파라미터 기록
    with open(os.path.join(output_path, 'params.json'), 'w') as f:
        f.write(json.dumps(vars(args)))

    # 로그 기록 설정
    file_handler = logging.FileHandler(filename=os.path.join(
        output_path, "{}.log".format(args.output_name)), encoding='utf-8')
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(format="%(message)s",
                        handlers=[file_handler, stream_handler], level=logging.DEBUG)

    # 로그, Keras Backend 설정을 먼저하고 RLTrader 모듈들을 이후에 임포트해야 함
    from agent import Agent
    from learners import DQNLearner

    # 모델 경로 준비
    value_network_path = ''
    policy_network_path = ''
    if args.value_network_name is not None:
        value_network_path = os.path.join(settings.BASE_DIR,
                                          'models/{}.h5'.format(args.value_network_name))
    else:
        value_network_path = os.path.join(
            output_path, '{}_{}_value_{}.h5'.format(
                args.rl_method, args.net, args.output_name))
    if args.policy_network_name is not None:
        policy_network_path = os.path.join(settings.BASE_DIR,
                                           'models/{}.h5'.format(args.policy_network_name))
    else:
        policy_network_path = os.path.join(
            output_path, '{}_{}_policy_{}.h5'.format(
                args.rl_method, args.net, args.output_name))

    common_params = {}
    list_stock_code = []
    list_chart_data = []
    list_training_data = []
    list_min_trading_unit = []
    list_max_trading_unit = []

    stock_code = args.stock_code

    get_data.get_data(stock_code,
                      args.start_date, args.end_date, ver=args.ver)

    # 차트 데이터, 학습 데이터 준비
    chart_data, training_data = data_manager.load_data(
        os.path.join(settings.BASE_DIR,
                     'data/{}/{}.csv'.format(args.ver, stock_code)),
        args.start_date, args.end_date, ver=args.ver)

    # 최소/최대 투자 단위 설정
    min_trading_unit = max(int(100000 / chart_data.iloc[-1]['close']), 1)
    max_trading_unit = max(int(1000000 / chart_data.iloc[-1]['close']), 1)

    # 공통 파라미터 설정
    common_params = {'rl_method': args.rl_method,
                     'delayed_reward_threshold': args.delayed_reward_threshold,
                     'net': args.net, 'num_steps': args.num_steps, 'lr': args.lr,
                     'output_path': output_path, 'reuse_models': args.reuse_models}

    # 강화학습 시작
    learner = None

    common_params.update({'stock_code': stock_code,
                          'chart_data': chart_data,
                          'training_data': training_data,
                          'min_trading_unit': min_trading_unit,
                          'max_trading_unit': max_trading_unit})

    learner = DQNLearner(**{**common_params,
                            'value_network_path': value_network_path})

    if learner is not None:
        pvs = learner.run(balance=args.balance,
                    num_epoches=args.num_epoches,
                    discount_factor=args.discount_factor,
                    start_epsilon=args.start_epsilon,
                    learning=args.learning)
        learner.save_models()

    return chart_data, pvs

def buyAndHold(chart_data):
    initial_price = chart_data.iloc[0, 1]
    numberOfStock = 100000 / initial_price
    priceHistory = chart_data['open'].to_list()
    print (priceHistory[0])
    buyAndHoldValue = [x * numberOfStock for x in priceHistory ]
    return buyAndHoldValue

if __name__ == '__main__':

    # #args = init(stock_code, num_epoches, num_steps)

    stock_names = ['GOOGL', 'AAPL', 'FB', 'AMZN', 'MSFT']

    for stock_name in stock_names :

        args = init(stock_name, 5, 5)
        chart_data, pvs = executor(args)
        buyAndHoldValue = buyAndHold(chart_data)
        visualizer.present_stock (chart_data, stock_name)
        visualizer.preset_buyAndHold(chart_data, pvs, buyAndHoldValue, stock_name)

        steps = [3,4,5,6,10]
        steps_pvs = []
        for step in steps :
            args = init(stock_name, 5, step)
            chart_data, pvs = executor(args)
            steps_pvs.append(pvs)
        visualizer.present_steps(chart_data, steps, steps_pvs, stock_name)

