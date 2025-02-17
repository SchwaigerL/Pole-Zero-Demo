from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from typing import Protocol
from scipy import signal

TODO: 'implement step response as well using  t,y = signal.dstep(sys3,n=30)'

side_frame_width = 140
all_fig_size = (5, 5)
theta = np.linspace(0, 2 * np.pi, 150)
radius = 1
grid_division = 11


@dataclass
class Model(Protocol):
    poles: list
    zeros: list
    freqs: list
    complex_f_resp: list


@dataclass
class Presenter(Protocol):
    model: Model

    def change_default_model(self, variable):
        ...

    def change_manual_model(self):
        ...


def create_freq_resp_plot(model):
    frequencies, freq_complex_resp = model.freqs, model.complex_f_resp
    fig, ax = plt.subplots(figsize=all_fig_size)
    ax.grid()
    x_values = frequencies
    y_values = np.abs(freq_complex_resp)
    ax.plot(x_values, y_values, label=f"frequency response")
    ax.set_title(f"frequency response")
    ax.set_xlabel("frequencies")
    ax.set_ylabel("response")
    # ax.legend()
    return fig, ax


def create_phase_resp_plot(model):
    frequencies, freq_complex_resp = model.freqs, model.complex_f_resp
    fig, ax = plt.subplots(figsize=all_fig_size)
    ax.grid()
    x_values = frequencies
    y_values = np.angle(freq_complex_resp)
    ax.plot(x_values, y_values, label=f"phase response")
    ax.set_title(f"phase response")
    ax.set_xlabel("frequencies")
    ax.set_ylabel("phase")
    # ax.legend()
    return fig, ax


def create_unit_circle():
    # plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    a = radius * np.cos(theta)
    b = radius * np.sin(theta)
    fig, ax = plt.subplots(figsize=all_fig_size)
    ax.grid()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.plot(a, b, c='b')
    return fig, ax


def create_freq_domain_plot(model):
    if model.type.name == 'DIGITAL':
        return create_z_plot(model)
    elif model.type.name == 'ANALOG':
        return create_s_plot(model)


def create_z_plot(model):
    assert model.type.name == 'DIGITAL', 'z plot only for descrete case'
    fig, ax = create_unit_circle()
    ax.grid()
    ax.set_title(f"Pole Zero map")
    for pole in model.poles:
        ax.scatter(np.real(pole), np.imag(pole), marker='X', color='r', s=100)
    for zero in model.zeros:
        ax.scatter(np.real(zero), np.imag(zero), marker='o', color='g', s=100)
    return fig, ax


def create_s_plot(model):
    assert model.type.name == 'ANALOG', 'S plot is only for continuous case'
    fig, ax = plt.subplots(figsize=all_fig_size)
    ax.grid()
    ax.set_ylim([-4, 4])
    ax.grid()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_title(f"Pole Zero map")
    for pole in model.poles:
        ax.scatter(np.real(pole), np.imag(pole), marker='X', color='r', s=100)
    for zero in model.zeros:
        ax.scatter(np.real(zero), np.imag(zero), marker='o', color='g', s=100)
    return fig, ax


def create_time_plot(model):
    if model.type.name == 'DIGITAL':
        return create_digital_impulse_time_response(model)
    elif model.type.name == 'ANALOG':
        return create_analog_impulse_time_response(model)


def create_digital_impulse_time_response(model):
    fig, ax = plt.subplots(figsize=all_fig_size)
    sys3 = signal.TransferFunction(model.num, model.denom, dt=0.1)
    # t,y = signal.dstep(sys3,n=30)
    t, y = signal.dimpulse(sys3, n=30)
    ax.step(t, np.squeeze(y))
    ax.grid()
    ax.set_xlabel('Number of samples')
    ax.set_ylabel('Amplitude')
    ax.set_title(f"Time response")
    return fig, ax


def create_analog_impulse_time_response(model):
    fig, ax = plt.subplots(figsize=all_fig_size)
    sys3 = signal.TransferFunction(model.num, model.denom)
    t, y = signal.impulse(sys3)
    ax.plot(t, y)
    ax.grid()
    ax.set_xlabel('time')
    ax.set_ylabel('Amplitude')
    ax.set_title(f"Time response")
    return fig, ax
