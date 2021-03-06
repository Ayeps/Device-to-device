from spectrum_allocation_power_control.topology import SingleCell
from spectrum_allocation_power_control.ddqn_keras import DDQNAgent

if __name__ == '__main__':
    slot_num = 500  # 循环次数
    radius = 500  # m
    cue_num = 20
    d2d_num = 20
    rb_num = 20
    up_or_down_link = 'up'
    d_tx2rx = 10  # m
    power_level_num = 10

    single_cell = SingleCell(radius, cue_num, d2d_num, rb_num, up_or_down_link, d_tx2rx, power_level_num)
    single_cell.initial()

    RL = DDQNAgent(4 * rb_num + 3, rb_num * power_level_num)
    # load weights
    RL.load('./save/ddqn2000_20*10.h5')

    sa_RL = DDQNAgent(4 * rb_num + 3, rb_num)
    sa_RL.load('./save/sa_ddqn2000.h5')

    for slot in range(slot_num):
        print("********************循环次数: ", slot, " ********************")
        single_cell.random_allocation_work(slot)
        single_cell.rl_test_work(slot, RL)
        single_cell.sa_test_work(slot, sa_RL)
        single_cell.q_learning_work(slot)
        single_cell.update()

    single_cell.save_data()
    single_cell.capacity(slot_num)
