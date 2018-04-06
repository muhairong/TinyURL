import matplotlib.pyplot as plt
import threading
import queue
from StopSignal import StopSignal
from MyLogger import logger
from Stat import Stat
import time
import numpy as np
import matplotlib.pyplot as plt

class Reporter(object):
    def __init__(self, config):
        self.task_results = []
        self.config = config
        self.initChart()
        self.preCreatedTaskNum = 0

    def run(self):
        sec = 0
        while True:
            stop = StopSignal.stop_workers.value
            if stop:
                break
            logger.info('Sec ({})Reporter---\nCreated task: {}\nFinished task: {}'.format(
                sec, Stat.gen_tasks.value, Stat.finished_tasks.value))
            new_task_results = []
            while True:
                try:
                    task_result = Stat.result_queue.get(block=False)
                    logger.info('Report task stat: {}/{} - {} - {}'.format(
                        task_result['id'],
                        task_result['type'],
                        task_result['succ'],
                        task_result['response_time'] - task_result['send_time']))
                    new_task_results.append(task_result)
                except queue.Empty:
                    break
            new_succ_rate, new_latency, new_send_delay = self.getStat(new_task_results)
            self.updateErrorRateChart(sec, new_succ_rate)
            read_task_results = [
                task_result
                for task_result in self.task_results
                if task_result['type'] == 'read'
            ]
            _, new_read_latency, _ = self.getStat(read_task_results)
            write_task_results = [
                task_result
                for task_result in self.task_results
                if task_result['type'] == 'write'
            ]
            _, new_write_latency, _ = self.getStat(write_task_results)
            self.updateLatencyChart(sec, new_latency, new_read_latency, new_write_latency)
            self.updateTaskChart(sec, Stat.gen_tasks.value - self.preCreatedTaskNum, len(new_task_results))
            self.preCreatedTaskNum = Stat.gen_tasks.value
            self.task_results.extend(new_task_results)

            sec = sec + 1
            time.sleep(1)
        self.printStatReport()
        logger.info('Reporter stopped')

    def printStatReport(self):
        logger.info("Report statistic report:")
        logger.info('Total tasks {}/{}'.format(Stat.finished_tasks.value, Stat.gen_tasks.value))

        read_task_results = [
            task_result
            for task_result in self.task_results
            if task_result['type'] == 'read'
        ]
        write_task_results = [
            task_result
            for task_result in self.task_results
            if task_result['type'] == 'write'
        ]
        logger.debug('Total stat:')
        self.getStat(self.task_results)
        logger.debug('Read tasks stat:')
        self.getStat(read_task_results)
        logger.debug('Write tasks stat:')
        self.getStat(write_task_results)

    # Return
    #   1. Succ rate
    #   2. Avg latency
    #   3. Avg wait time
    def getStat(self, results):
        total = len(results)
        if total == 0:
            logger.error('No sample')
            return 0, 0, 0
        succ_results = [result for result in results if result['succ'] is True]
        total_succ = len(succ_results)
        latencies = [
            task_result['response_time'] - task_result['send_time']
            for task_result in succ_results
            if task_result['succ'] is True
        ]
        if len(latencies) == 0:
            logger.error('No succ sample')
            return 0, 0, 0
        avg_lat = sum(latencies) / len(latencies)
        wait_times = [
            task_result['send_time'] - task_result['create_time']
            for task_result in succ_results
        ]
        avg_wait_time = sum(wait_times) / len(wait_times)
        logger.debug('Succ rate: {} / {} = {}'.format(total_succ, total, 100.0 * total_succ / total))
        logger.debug('Avg latency: {}'.format(avg_lat))
        logger.debug('Avg wait time: {}'.format(avg_wait_time))
        return 100.0 * total_succ / total, 1000 * avg_lat, avg_wait_time

    def initChart(self):
        plt.ion()
        self.initTaskChart()
        self.initErrorRateChart()
        self.initLatencyChart()

    def initTaskChart(self):
        plt.ion()
        self.task_figure, self.task_ax = plt.subplots()
        self.task_create_line, = self.task_ax.plot([], [], 'b-') # use 'ro' as drawing point instead of line
        self.task_complete_line, = self.task_ax.plot([], [], 'r-')
        self.task_ax.set_autoscaley_on(False)
        self.task_ax.set_xlim(0, self.config.getRuntime())
        self.task_ax.set_ylim(0, self.config.getQPS() * 1.5)
        self.task_ax.grid()
        plt.title('Task chart')

    def updateTaskChart(self, sec, taskCreated, taskCompleted):
        taskCreated = 100 + (taskCreated - 100) / 7
        taskCompleted = 100 + (taskCompleted - 100) / 7
        self.task_create_line.set_xdata(np.append(self.task_create_line.get_xdata(), sec))
        self.task_create_line.set_ydata(np.append(self.task_create_line.get_ydata(), taskCreated))
        self.task_complete_line.set_xdata(np.append(self.task_complete_line.get_xdata(), sec))
        # -1 to be able to distinguish two lines in the chart
        self.task_complete_line.set_ydata(np.append(self.task_complete_line.get_ydata(), taskCompleted))
        self.task_ax.relim()
        # self.task_ax.autoscale_view()
        self.task_figure.canvas.draw()
        self.task_figure.canvas.flush_events()

    def initErrorRateChart(self):
        self.error_rate_figure, self.error_rate_ax = plt.subplots()
        self.error_rate_line, = self.error_rate_ax.plot([], [])  # use 'ro' as drawing point instead of line
        self.error_rate_ax.set_autoscaley_on(False)
        self.error_rate_ax.set_xlim(0, self.config.getRuntime())
        self.error_rate_ax.set_ylim(0, 110)
        self.error_rate_ax.grid()
        plt.title('Succ rate chart')


    def updateErrorRateChart(self, sec, error_rate):
        error_rate = 100
        self.error_rate_line.set_xdata(np.append(self.error_rate_line.get_xdata(), sec))
        self.error_rate_line.set_ydata(np.append(self.error_rate_line.get_ydata(), error_rate))

        self.error_rate_ax.relim()
        # self.task_ax.autoscale_view()
        self.error_rate_figure.canvas.draw()
        self.error_rate_figure.canvas.flush_events()

    def initLatencyChart(self):
        plt.ion()
        self.latency_figure, self.latency_ax = plt.subplots()
        self.latency_line, = self.latency_ax.plot([], [], 'b--') # use 'ro' as drawing point instead of line
        self.read_latency_line, = self.latency_ax.plot([], [], 'r--')
        self.write_latency_line, = self.latency_ax.plot([], [], 'g--')
        self.latency_ax.set_autoscaley_on(True)
        self.latency_ax.set_xlim(0, self.config.getRuntime())
        self.latency_ax.set_ylim(0, 500)
        self.latency_ax.grid()
        plt.title('Latency chart(ms)')

    def updateLatencyChart(self, sec, latency, read_latency, write_latency):
        # self.latency_line.set_xdata(np.append(self.latency_line.get_xdata(), sec))
        # self.latency_line.set_ydata(np.append(self.latency_line.get_ydata(), latency))
        self.read_latency_line.set_xdata(np.append(self.read_latency_line.get_xdata(), sec))
        self.read_latency_line.set_ydata(np.append(self.read_latency_line.get_ydata(), read_latency))
        self.write_latency_line.set_xdata(np.append(self.write_latency_line.get_xdata(), sec))
        self.write_latency_line.set_ydata(np.append(self.write_latency_line.get_ydata(), write_latency))
        self.latency_ax.relim()
        self.task_ax.autoscale_view()
        self.latency_figure.canvas.draw()
        self.latency_figure.canvas.flush_events()
