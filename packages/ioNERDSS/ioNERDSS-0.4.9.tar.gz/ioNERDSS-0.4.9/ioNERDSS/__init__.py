import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
import sys
import copy

# ---------------------------------Platonic Solid Model--------------------------------------


def distance(a: float, b: float):
    # a seperated function for calculating the distance between two coordinates
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)


def mid_pt(a: float, b: float):
    # this is a seperate function for calculating mid point of two coords
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]


def angle_cal(COM1: float, leg1: float, COM2: float, leg2: float):
    n = 8
    c1 = np.array(COM1)
    p1 = np.array(leg1)
    c2 = np.array(COM2)
    p2 = np.array(leg2)
    v1 = p1 - c1
    v2 = p2 - c2
    sig1 = p1 - p2
    sig2 = -sig1
    theta1 = round(math.acos(np.dot(v1, sig1) /
                   (np.linalg.norm(v1)*np.linalg.norm(sig1))), n)
    theta2 = round(math.acos(np.dot(v2, sig2) /
                   (np.linalg.norm(v2)*np.linalg.norm(sig2))), n)
    t1 = np.cross(v1, sig1)
    t2 = np.cross(v1, c1)  # n1 = c1 here
    t1_hat = t1/np.linalg.norm(t1)
    t2_hat = t2/np.linalg.norm(t2)
    phi1 = round(math.acos(np.around(np.dot(t1_hat, t2_hat), n)), n)
    t3 = np.cross(v2, sig2)
    t4 = np.cross(v2, c2)  # n2 = c2 here
    t3_hat = t3/np.linalg.norm(t3)
    t4_hat = t4/np.linalg.norm(t4)
    phi2 = round(math.acos(np.around(np.dot(t3_hat, t4_hat), n)), n)
    t1_ = np.cross(sig1, v1)
    t2_ = np.cross(sig1, v2)
    t1__hat = t1_/np.linalg.norm(t1_)
    t2__hat = t2_/np.linalg.norm(t2_)
    omega = round(math.acos(np.around(np.dot(t1__hat, t2__hat), n)), n)
    return theta1, theta2, phi1, phi2, omega


# DODECAHEDEON FACE AS COM

def dode_face_dodecahedron_coord(radius: float):
    # Setup coordinates of 20 verticies when scaler = 1
    scaler = radius/(3**0.5)
    m = (1+5**(0.5))/2
    V1 = [0, m, 1/m]
    V2 = [0, m, -1/m]
    V3 = [0, -m, 1/m]
    V4 = [0, -m, -1/m]
    V5 = [1/m, 0, m]
    V6 = [1/m, 0, -m]
    V7 = [-1/m, 0, m]
    V8 = [-1/m, 0, -m]
    V9 = [m, 1/m, 0]
    V10 = [m, -1/m, 0]
    V11 = [-m, 1/m, 0]
    V12 = [-m, -1/m, 0]
    V13 = [1, 1, 1]
    V14 = [1, 1, -1]
    V15 = [1, -1, 1]
    V16 = [1, -1, -1]
    V17 = [-1, 1, 1]
    V18 = [-1, 1, -1]
    V19 = [-1, -1, 1]
    V20 = [-1, -1, -1]
    coord = [V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
             V11, V12, V13, V14, V15, V16, V17, V18, V19, V20]
    # calculate coordinates according to the scaler as coord_ (list)
    coord_ = []
    for i in coord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        coord_.append(temp_list)
    return coord_


def dode_face_COM_coor(a: float, b: float, c: float, d: float, e: float):
    # calculate the center of mass(COM) according to 5 coords on the same face
    n = 10
    mid_a = mid_pt(c, d)
    mid_b = mid_pt(d, e)
    mid_c = mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    # calculate 3 COM here and check if they are overlapped
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
    # checking overlap
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and \
        round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and \
            round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        return COM_a
    else:
        return COM_a


def dode_face_COM_list_gen(radius: float):
    # generate the list of COM of all 12 faces
    coord = dode_face_dodecahedron_coord(radius)
    COM_list = []
    COM_list.append(dode_face_COM_coor(
        coord[6], coord[18], coord[2], coord[14], coord[4]))
    COM_list.append(dode_face_COM_coor(
        coord[6], coord[4], coord[12], coord[0], coord[16]))
    COM_list.append(dode_face_COM_coor(
        coord[4], coord[14], coord[9], coord[8], coord[12]))
    COM_list.append(dode_face_COM_coor(
        coord[6], coord[18], coord[11], coord[10], coord[16]))
    COM_list.append(dode_face_COM_coor(
        coord[14], coord[2], coord[3], coord[15], coord[9]))
    COM_list.append(dode_face_COM_coor(
        coord[18], coord[11], coord[19], coord[3], coord[2]))
    COM_list.append(dode_face_COM_coor(
        coord[16], coord[10], coord[17], coord[1], coord[0]))
    COM_list.append(dode_face_COM_coor(
        coord[12], coord[0], coord[1], coord[13], coord[8]))
    COM_list.append(dode_face_COM_coor(
        coord[7], coord[17], coord[10], coord[11], coord[19]))
    COM_list.append(dode_face_COM_coor(
        coord[5], coord[13], coord[8], coord[9], coord[15]))
    COM_list.append(dode_face_COM_coor(
        coord[3], coord[19], coord[7], coord[5], coord[15]))
    COM_list.append(dode_face_COM_coor(
        coord[1], coord[17], coord[7], coord[5], coord[13]))
    return COM_list


def dode_face_COM_leg_coor(a: float, b: float, c: float, d: float, e: float):
    # calculate COM and 5 legs of one protein, 6 coords in total [COM, lg1, lg2, lg3, lg4, lg5]
    COM_leg = []
    COM_leg.append(dode_face_COM_coor(a, b, c, d, e))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, e))
    COM_leg.append(mid_pt(e, a))
    return COM_leg


def dode_face_COM_leg_list_gen(radius: float):
    # generate all COM and leg coords of 12 faces as a large list
    coord = dode_face_dodecahedron_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[18], coord[2], coord[14], coord[4]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[4], coord[12], coord[0], coord[16]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[4], coord[14], coord[9], coord[8], coord[12]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[6], coord[18], coord[11], coord[10], coord[16]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[14], coord[2], coord[3], coord[15], coord[9]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[18], coord[11], coord[19], coord[3], coord[2]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[16], coord[10], coord[17], coord[1], coord[0]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[12], coord[0], coord[1], coord[13], coord[8]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[7], coord[17], coord[10], coord[11], coord[19]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[5], coord[13], coord[8], coord[9], coord[15]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[3], coord[19], coord[7], coord[5], coord[15]))
    COM_leg_list.append(dode_face_COM_leg_coor(
        coord[1], coord[17], coord[7], coord[5], coord[13]))
    return COM_leg_list


def dode_face_leg_reduce(COM: float, leg: float, sigma: float):
    # calculate the recuced length when considering the sigma value
    n = 14
    m = (1+5**(0.5))/2
    angle = 2*math.atan(m)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def dode_face_leg_reduce_coor_gen(radius: float, sigma: float):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = dode_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(dode_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def dode_face_input_coord(radius: float, sigma: float):
    coor = dode_face_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    lg5 = coor_[5] - coor_[0]
    n = -coor_[0]
    return COM, lg1, lg2, lg3, lg4, lg5, n


def dode_face_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, lg4, lg5, n = dode_face_input_coord(radius, sigma)
    coord = dode_face_leg_reduce_coor_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][3], coord[4][0], coord[4][1])

    f = open('parm.inp', 'w')
    f.write(' # Input file (dodecahedron face-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    dode : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    dode(lg1) + dode(lg1) <-> dode(lg1!1).dode(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg2) <-> dode(lg2!1).dode(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg3) + dode(lg3) <-> dode(lg3!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg4) + dode(lg4) <-> dode(lg4!1).dode(lg4!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg5) + dode(lg5) <-> dode(lg5!1).dode(lg5!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg2) <-> dode(lg1!1).dode(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg3) <-> dode(lg1!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg4) <-> dode(lg1!1).dode(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg5) <-> dode(lg1!1).dode(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg3) <-> dode(lg2!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg4) <-> dode(lg2!1).dode(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg5) <-> dode(lg2!1).dode(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg3) + dode(lg4) <-> dode(lg3!1).dode(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg3) + dode(lg5) <-> dode(lg3!1).dode(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg4) + dode(lg5) <-> dode(lg4!1).dode(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('dode.mol', 'w')
    f.write('##\n')
    f.write('# Dodecahedron (face-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = dode\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
            str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
    f.write('lg5   ' + str(round(lg5[0], 8)) + '   ' +
            str(round(lg5[1], 8)) + '   ' + str(round(lg5[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 5\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('com lg4\n')
    f.write('com lg5\n')
    f.write('\n')


# DODECAHEDEON VERTEX AS COM

def dode_vert_coord(radius: float):
    scaler = radius/(3**0.5)
    m = (1+5**(0.5))/2
    V0 = [0, m, 1/m]
    V1 = [0, m, -1/m]
    V2 = [0, -m, 1/m]
    V3 = [0, -m, -1/m]
    V4 = [1/m, 0, m]
    V5 = [1/m, 0, -m]
    V6 = [-1/m, 0, m]
    V7 = [-1/m, 0, -m]
    V8 = [m, 1/m, 0]
    V9 = [m, -1/m, 0]
    V10 = [-m, 1/m, 0]
    V11 = [-m, -1/m, 0]
    V12 = [1, 1, 1]
    V13 = [1, 1, -1]
    V14 = [1, -1, 1]
    V15 = [1, -1, -1]
    V16 = [-1, 1, 1]
    V17 = [-1, 1, -1]
    V18 = [-1, -1, 1]
    V19 = [-1, -1, -1]
    coord = [V0, V1, V2, V3, V4, V5, V6, V7, V8, V9,
             V10, V11, V12, V13, V14, V15, V16, V17, V18, V19]
    coord_ = []
    for i in coord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        coord_.append(temp_list)
    return coord_


def dode_vert_COM_leg(COM: float, a: float, b: float, c: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


def dode_vert_COM_leg_gen(radius: float):
    coord = dode_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(dode_vert_COM_leg(
        coord[0], coord[1], coord[12], coord[16]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[1], coord[0], coord[13], coord[17]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[2], coord[3], coord[14], coord[18]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[3], coord[2], coord[15], coord[19]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[4], coord[6], coord[12], coord[14]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[5], coord[7], coord[13], coord[15]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[6], coord[4], coord[16], coord[18]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[7], coord[5], coord[17], coord[19]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[8], coord[9], coord[12], coord[13]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[9], coord[8], coord[14], coord[15]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[10], coord[11], coord[16], coord[17]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[11], coord[10], coord[18], coord[19]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[12], coord[0], coord[4], coord[8]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[13], coord[1], coord[5], coord[8]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[14], coord[2], coord[4], coord[9]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[15], coord[3], coord[5], coord[9]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[16], coord[0], coord[6], coord[10]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[17], coord[1], coord[7], coord[10]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[18], coord[2], coord[6], coord[11]))
    COM_leg_list.append(dode_vert_COM_leg(
        coord[19], coord[3], coord[7], coord[11]))
    return COM_leg_list


def dode_vert_leg_reduce(COM: float, leg: float, sigma: float):
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def dode_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    COM_leg_list = dode_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(dode_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def dode_vert_input_coord(radius: float, sigma: float):
    coor = dode_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, n


def dode_vert_norm_input(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = dode_vert_input_coord(radius, sigma)
    length = distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


def dode_vert_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = dode_vert_norm_input(radius, sigma)
    f = open('parm.inp', 'w')
    f.write(' # Input file (dodecahedron vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    dode : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    dode(lg1) + dode(lg1) <-> dode(lg1!1).dode(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg2) <-> dode(lg2!1).dode(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg3) + dode(lg3) <-> dode(lg3!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg2) <-> dode(lg1!1).dode(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg1) + dode(lg3) <-> dode(lg1!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    dode(lg2) + dode(lg3) <-> dode(lg2!1).dode(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('dode.mol', 'w')
    f.write('##\n')
    f.write('# Dodecahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = dode\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


# ICOSAHEDRON FACE AS COM

def icos_face_vert_coord(radius: float):
    scaler = radius/(2*math.sin(2*math.pi/5))
    m = (1+5**0.5)/2
    v0 = [0, 1, m]
    v1 = [0, 1, -m]
    v2 = [0, -1, m]
    v3 = [0, -1, -m]
    v4 = [1, m, 0]
    v5 = [1, -m, 0]
    v6 = [-1, m, 0]
    v7 = [-1, -m, 0]
    v8 = [m, 0, 1]
    v9 = [m, 0, -1]
    v10 = [-m, 0, 1]
    v11 = [-m, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def icos_face_COM_coord(a: float, b: float, c: float):
    mid_a = mid_pt(b, c)
    mid_b = mid_pt(a, c)
    mid_c = mid_pt(a, b)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
    if COM_a == COM_b and COM_b == COM_c:
        return COM_a
    else:
        return COM_a


def icos_face_COM_list_gen(radius: float):
    coord = icos_face_vert_coord(radius)
    COM_list = []
    COM_list.append(icos_face_COM_coord(coord[0], coord[2], coord[8]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[8], coord[4]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[4], coord[6]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[6], coord[10]))
    COM_list.append(icos_face_COM_coord(coord[0], coord[10], coord[2]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[7], coord[5]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[5], coord[9]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[9], coord[1]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[1], coord[11]))
    COM_list.append(icos_face_COM_coord(coord[3], coord[11], coord[7]))
    COM_list.append(icos_face_COM_coord(coord[7], coord[2], coord[5]))
    COM_list.append(icos_face_COM_coord(coord[2], coord[5], coord[8]))
    COM_list.append(icos_face_COM_coord(coord[5], coord[8], coord[9]))
    COM_list.append(icos_face_COM_coord(coord[8], coord[9], coord[4]))
    COM_list.append(icos_face_COM_coord(coord[9], coord[4], coord[1]))
    COM_list.append(icos_face_COM_coord(coord[4], coord[1], coord[6]))
    COM_list.append(icos_face_COM_coord(coord[1], coord[6], coord[11]))
    COM_list.append(icos_face_COM_coord(coord[6], coord[11], coord[10]))
    COM_list.append(icos_face_COM_coord(coord[11], coord[10], coord[7]))
    COM_list.append(icos_face_COM_coord(coord[10], coord[7], coord[2]))
    return COM_list


def icos_face_COM_leg_coord(a: float, b: float, c: float):
    COM_leg = []
    COM_leg.append(icos_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


def COM_leg_list_gen(radius: float):
    coord = icos_face_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[2], coord[8]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[8], coord[4]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[4], coord[6]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[6], coord[10]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[10], coord[2]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[7], coord[5]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[5], coord[9]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[9], coord[1]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[1], coord[11]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[11], coord[7]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[7], coord[2], coord[5]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[2], coord[5], coord[8]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[5], coord[8], coord[9]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[8], coord[9], coord[4]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[9], coord[4], coord[1]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[4], coord[1], coord[6]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[1], coord[6], coord[11]))
    COM_leg_list.append(icos_face_COM_leg_coord(
        coord[6], coord[11], coord[10]))
    COM_leg_list.append(icos_face_COM_leg_coord(
        coord[11], coord[10], coord[7]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[10], coord[7], coord[2]))
    return COM_leg_list


def icos_face_leg_reduce(COM: float, leg: float, sigma: float):
    n = 12
    angle = math.acos(-5**0.5/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def icos_face_leg_reduce_coord_gen(radius: float, sigma: float):
    COM_leg_list = COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(icos_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def icos_face_input_coord(radius: float, sigma: float):
    coor = icos_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


def icos_face_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = icos_face_input_coord(radius, sigma)
    coord = icos_face_leg_reduce_coord_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][2], coord[11][0], coord[11][3])

    f = open('parm.inp', 'w')
    f.write(' # Input file (icosahedron face-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    dode : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    icos(lg1) + icos(lg1) <-> icos(lg1!1).icos(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg2) <-> icos(lg2!1).icos(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg3) + icos(lg3) <-> icos(lg3!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg2) <-> icos(lg1!1).icos(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg3) <-> icos(lg1!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg3) <-> icos(lg2!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('icos.mol', 'w')
    f.write('##\n')
    f.write('# Icosahehedron (face-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = icos\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


# ICOSAHEDRON VERTEX AS COM

def icos_vert_coord(radius: float):
    scaler = radius/(2*math.sin(2*math.pi/5))
    m = (1+5**0.5)/2
    v0 = [0, 1, m]
    v1 = [0, 1, -m]
    v2 = [0, -1, m]
    v3 = [0, -1, -m]
    v4 = [1, m, 0]
    v5 = [1, -m, 0]
    v6 = [-1, m, 0]
    v7 = [-1, -m, 0]
    v8 = [m, 0, 1]
    v9 = [m, 0, -1]
    v10 = [-m, 0, 1]
    v11 = [-m, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def icos_vert_COM_leg(COM: float, a: float, b: float, c: float, d: float, e: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    legd = mid_pt(COM, d)
    lege = mid_pt(COM, e)
    result = [np.around(COM, 10), np.around(lega, 10), np.around(
        legb, 10), np. around(legc, 10), np.around(legd, 10), np.around(lege, 10)]
    return result


def icos_vert_COM_leg_gen(radius: float):
    coord = icos_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(icos_vert_COM_leg(
        coord[0], coord[2], coord[8], coord[4], coord[6], coord[10]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[1], coord[4], coord[6], coord[11], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[2], coord[0], coord[10], coord[7], coord[5], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[3], coord[1], coord[11], coord[7], coord[5], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[4], coord[0], coord[6], coord[1], coord[9], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[5], coord[2], coord[8], coord[7], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[6], coord[0], coord[10], coord[11], coord[1], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[7], coord[3], coord[11], coord[10], coord[2], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[8], coord[0], coord[2], coord[5], coord[9], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[9], coord[8], coord[4], coord[1], coord[3], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[10], coord[0], coord[2], coord[7], coord[11], coord[6]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[11], coord[10], coord[7], coord[3], coord[1], coord[6]))
    return COM_leg_list


def icos_vert_leg_reduce(COM: float, leg: float, sigma: float):
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def icos_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    COM_leg_list = icos_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(icos_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def icos_vert_input_coord(radius: float, sigma: float):
    coor = icos_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    lg4 = np.around(coor_[4] - coor_[0], 12)
    lg5 = np.around(coor_[5] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, lg4, lg5, n


def icos_vert_center_coor(a: float, b: float, c: float, d: float, e: float):
    n = 8
    mid_a = mid_pt(c, d)
    mid_b = mid_pt(d, e)
    mid_c = mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and \
        round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and \
            round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        return COM_a
    else:
        return COM_a


def icos_vert_check_dis(cen: float, COM: float, lg1: float, lg2: float, lg3: float, lg4: float, lg5: float):
    dis1 = round(distance(cen, lg1), 8)
    dis2 = round(distance(cen, lg2), 8)
    dis3 = round(distance(cen, lg3), 8)
    dis4 = round(distance(cen, lg4), 8)
    dis5 = round(distance(cen, lg5), 8)
    dis_ = round(distance(COM, cen), 8)
    if dis1 == dis2 and dis1 == dis3 and dis1 == dis4 and dis1 == dis5:
        return dis1, dis_
    else:
        return dis1, dis_


def icos_vert_norm_input(scaler: float, dis_: float):
    c1 = math.cos(2*math.pi/5)
    c2 = math.cos(math.pi/5)
    s1 = math.sin(2*math.pi/5)
    s2 = math.sin(4*math.pi/5)
    v0 = scaler*np.array([0, 1])
    v1 = scaler*np.array([-s1, c1])
    v2 = scaler*np.array([-s2, -c2])
    v3 = scaler*np.array([s2, -c2])
    v4 = scaler*np.array([s1, c1])
    lg1 = np.array([v0[0], v0[1], -dis_])
    lg2 = np.array([v1[0], v1[1], -dis_])
    lg3 = np.array([v2[0], v2[1], -dis_])
    lg4 = np.array([v3[0], v3[1], -dis_])
    lg5 = np.array([v4[0], v4[1], -dis_])
    COM = np.array([0, 0, 0])
    n = np.array([0, 0, 1])
    return COM, lg1, lg2, lg3, lg4, lg5, n


def icos_vert_write(radius: float, sigma: float):
    COM_, lg1_, lg2_, lg3_, lg4_, lg5_, n_ = icos_vert_input_coord(
        radius, sigma)
    cen_ = icos_vert_center_coor(lg1_, lg2_, lg3_, lg4_, lg5_)
    scaler, dis_ = icos_vert_check_dis(
        cen_, COM_, lg1_, lg2_, lg3_, lg4_, lg5_)
    COM, lg1, lg2, lg3, lg4, lg5, n = icos_vert_norm_input(scaler, dis_)

    f = open('parm.inp', 'w')
    f.write(' # Input file (icosahedron vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    icos : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    icos(lg1) + icos(lg1) <-> icos(lg1!1).icos(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg2) <-> icos(lg2!1).icos(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg3) + icos(lg3) <-> icos(lg3!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg4) + icos(lg4) <-> icos(lg4!1).icos(lg4!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg5) + icos(lg5) <-> icos(lg5!1).icos(lg5!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg2) <-> icos(lg1!1).icos(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg3) <-> icos(lg1!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg4) <-> icos(lg1!1).icos(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg1) + icos(lg5) <-> icos(lg1!1).icos(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg3) <-> icos(lg2!1).icos(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg4) <-> icos(lg2!1).icos(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg2) + icos(lg5) <-> icos(lg2!1).icos(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg3) + icos(lg4) <-> icos(lg3!1).icos(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg3) + icos(lg5) <-> icos(lg3!1).icos(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    icos(lg4) + icos(lg5) <-> icos(lg4!1).icos(lg5!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('icos.mol', 'w')
    f.write('##\n')
    f.write('# Icosahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = icos\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
            str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
    f.write('lg5   ' + str(round(lg5[0], 8)) + '   ' +
            str(round(lg5[1], 8)) + '   ' + str(round(lg5[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 5\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('com lg4\n')
    f.write('com lg5\n')
    f.write('\n')


# OCTAHEDRON FACE AS COM

def octa_face_vert_coord(radius: float):
    scaler = radius
    v0 = [1, 0, 0]
    v1 = [-1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [0, -1, 0]
    v4 = [0, 0, 1]
    v5 = [0, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def octa_face_COM_coord(a: float, b: float, c: float):
    mid_a = mid_pt(b, c)
    mid_b = mid_pt(a, c)
    mid_c = mid_pt(a, b)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
    if COM_a == COM_b and COM_b == COM_c:
        return COM_a
    else:
        return COM_a


def octa_face_COM_list_gen(radius: float):
    coord = octa_face_vert_coord(radius)
    COM_list = []
    COM_list.append(octa_face_COM_coord(coord[0], coord[2], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[3], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[3], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[0], coord[2], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[2], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[3], coord[4]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[3], coord[5]))
    COM_list.append(octa_face_COM_coord(coord[1], coord[2], coord[5]))
    return COM_list


def octa_face_COM_leg_coord(a: float, b: float, c: float):
    COM_leg = []
    COM_leg.append(octa_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


def octa_face_COM_leg_list_gen(radius: float):
    coord = octa_face_vert_coord(radius)
    COM_leg_list = []

    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[5]))
    return COM_leg_list


def octa_face_leg_reduce(COM: float, leg: float, sigma: float):
    n = 12
    angle = math.acos(-1/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def octa_face_leg_reduce_coord_gen(radius: float, sigma: float):
    COM_leg_list = octa_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(octa_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def octa_face_input_coord(radius: float, sigma: float):
    coor = octa_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


def octa_face_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = octa_face_input_coord(radius, sigma)
    coord = octa_face_leg_reduce_coord_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][3], coord[1][0], coord[1][3])

    f = open('parm.inp', 'w')
    f.write(' # Input file (octahedron face-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    octa : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    octa(lg1) + octa(lg1) <-> octa(lg1!1).octa(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    octa(lg2) + octa(lg2) <-> octa(lg2!1).octa(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    octa(lg3) + octa(lg3) <-> octa(lg3!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    octa(lg1) + octa(lg2) <-> octa(lg1!1).octa(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    octa(lg1) + octa(lg3) <-> octa(lg1!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    octa(lg2) + octa(lg3) <-> octa(lg2!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('octa.mol', 'w')
    f.write('##\n')
    f.write('# Octahehedron (face-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = octa\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


# OCTAHEDRON VERTEX AS COM

def octa_vert_coord(radius: float):
    scaler = radius
    v0 = [1, 0, 0]
    v1 = [-1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [0, -1, 0]
    v4 = [0, 0, 1]
    v5 = [0, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def octa_vert_COM_leg(COM: float, a: float, b: float, c: float, d: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    legd = mid_pt(COM, d)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10), np.around(legd, 10)]


def octa_vert_COM_leg_gen(radius: float):
    coord = octa_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(octa_vert_COM_leg(
        coord[0], coord[2], coord[4], coord[3], coord[5]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[1], coord[2], coord[4], coord[3], coord[5]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[2], coord[1], coord[5], coord[0], coord[4]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[3], coord[1], coord[5], coord[0], coord[4]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[4], coord[1], coord[2], coord[0], coord[3]))
    COM_leg_list.append(octa_vert_COM_leg(
        coord[5], coord[1], coord[2], coord[0], coord[3]))
    return COM_leg_list


def octa_vert_leg_reduce(COM: float, leg: float, sigma: float):
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def octa_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    COM_leg_list = octa_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 4:
            temp_list.append(octa_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def octa_vert_input_coord(radius: float, sigma: float):
    coor = octa_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[4])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    lg4 = np.around(coor_[4] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, lg4, n


def octa_vert_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, lg4, n = octa_vert_input_coord(radius, sigma)
    f = open('parm.inp', 'w')
    f.write(' # Input file (octahedron vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    octa : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    otca(lg1) + octa(lg1) <-> octa(lg1!1).octa(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg2) + octa(lg2) <-> octa(lg2!1).octa(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg3) + octa(lg3) <-> octa(lg3!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg4) + octa(lg4) <-> octa(lg4!1).octa(lg4!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg1) + octa(lg2) <-> octa(lg1!1).octa(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg1) + octa(lg3) <-> octa(lg1!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg1) + octa(lg4) <-> octa(lg1!1).octa(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg2) + octa(lg3) <-> octa(lg2!1).octa(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg2) + octa(lg4) <-> octa(lg2!1).octa(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    otca(lg3) + octa(lg4) <-> octa(lg3!1).octa(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('octa.mol', 'w')
    f.write('##\n')
    f.write('# Octahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = octa\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
            str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 4\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('com lg4\n')
    f.write('\n')


# CUBE FACE AS COM

def cube_face_vert_coord(radius: float):
    scaler = radius/3**0.5
    v0 = [1, 1, 1]
    v1 = [-1, 1, 1]
    v2 = [1, -1, 1]
    v3 = [1, 1, -1]
    v4 = [-1, -1, 1]
    v5 = [1, -1, -1]
    v6 = [-1, 1, -1]
    v7 = [-1, -1, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def cube_face_COM_coord(a: float, b: float, c: float, d: float):
    mid_a = mid_pt(a, b)
    mid_b = mid_pt(b, c)
    mid_c = mid_pt(c, d)
    mid_d = mid_pt(d, a)
    COM_a = mid_pt(mid_a, mid_c)
    COM_b = mid_pt(mid_b, mid_d)
    if COM_a == COM_b:
        return COM_a
    else:
        return COM_a


def cube_face_COM_list_gen(radius: float):
    coord = cube_face_vert_coord(radius)
    COM_list = []
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[5], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[6], coord[1]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[1], coord[4], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[1], coord[6]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[2], coord[5]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[6], coord[3], coord[5]))
    return COM_list


def cube_face_COM_leg_coord(a: float, b: float, c: float, d: float):
    COM_leg = []
    COM_leg.append(cube_face_COM_coord(a, b, c, d))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, a))
    return COM_leg


def cube_face_COM_leg_list_gen(radius: float):
    coord = cube_face_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[3], coord[5], coord[2]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[3], coord[6], coord[1]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[0], coord[1], coord[4], coord[2]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[4], coord[1], coord[6]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[4], coord[2], coord[5]))
    COM_leg_list.append(cube_face_COM_leg_coord(
        coord[7], coord[6], coord[3], coord[5]))
    return COM_leg_list


def cube_face_leg_reduce(COM: float, leg: float, sigma: float):
    n = 12
    angle = math.acos(0)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def cube_face_leg_reduce_coord_gen(radius: float, sigma: float):
    COM_leg_list = cube_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(np.around(elements[0], 8))
        i = 1
        while i <= 4:
            temp_list.append(np.around(cube_face_leg_reduce(
                elements[0], elements[i], sigma), 8))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def cube_face_input_coord(radius: float, sigma: float):
    coor = cube_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 7)
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, lg4, n]


def cube_face_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, lg4, n = cube_face_input_coord(radius, sigma)
    coord = cube_face_leg_reduce_coord_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][1], coord[1][0], coord[1][1])

    f = open('parm.inp', 'w')
    f.write(' # Input file (cube face-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    cube : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    cube(lg1) + cube(lg1) <-> cube(lg1!1).cube(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg2) + cube(lg2) <-> cube(lg2!1).cube(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg3) + cube(lg3) <-> cube(lg3!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg4) + cube(lg4) <-> cube(lg4!1).cube(lg4!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg1) + cube(lg2) <-> cube(lg1!1).cube(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg1) + cube(lg3) <-> cube(lg1!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg1) + cube(lg4) <-> cube(lg1!1).cube(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg2) + cube(lg3) <-> cube(lg2!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg2) + cube(lg4) <-> cube(lg2!1).cube(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg3) + cube(lg4) <-> cube(lg3!1).cube(lg4!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('cube.mol', 'w')
    f.write('##\n')
    f.write('# Cube (face-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = cube\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
            str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 4\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('com lg4\n')
    f.write('\n')


# CUBE VERTEX AS COM

def cube_vert_coord(radius: float):
    scaler = radius/3**0.5
    v0 = [1, 1, 1]
    v1 = [-1, 1, 1]
    v2 = [1, -1, 1]
    v3 = [1, 1, -1]
    v4 = [-1, -1, 1]
    v5 = [1, -1, -1]
    v6 = [-1, 1, -1]
    v7 = [-1, -1, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def cube_vert_COM_leg(COM: float, a: float, b: float, c: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


def cube_vert_COM_leg_gen(radius: float):
    coord = cube_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(cube_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[1], coord[0], coord[4], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[2], coord[0], coord[4], coord[5]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[3], coord[0], coord[5], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[4], coord[1], coord[2], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[5], coord[2], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[6], coord[1], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[7], coord[4], coord[5], coord[6]))
    return COM_leg_list


def cube_vert_leg_reduce(COM: float, leg: float, sigma: float):
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def cube_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    COM_leg_list = cube_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(cube_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def cube_vert_input_coord(radius: float, sigma: float):
    coor = cube_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, n


def cube_vert_norm_input(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = cube_vert_input_coord(radius, sigma)
    length = distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


def cube_vert_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = cube_vert_norm_input(radius, sigma)
    f = open('parm.inp', 'w')
    f.write(' # Input file (cube vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    cube : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    cube(lg1) + cube(lg1) <-> cube(lg1!1).cube(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg2) + cube(lg2) <-> cube(lg2!1).cube(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg3) + cube(lg3) <-> cube(lg3!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg1) + cube(lg2) <-> cube(lg1!1).cube(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg1) + cube(lg3) <-> cube(lg1!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    cube(lg2) + cube(lg3) <-> cube(lg2!1).cube(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('cube.mol', 'w')
    f.write('##\n')
    f.write('# Cube (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = cube\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


# TETRAHETRON FACE AS COM

def tetr_face_coord(radius: float):
    scaler = radius/(3/8)**0.5/2
    v0 = [1, 0, -1/2**0.5]
    v1 = [-1, 0, -1/2**0.5]
    v2 = [0, 1, 1/2**0.5]
    v3 = [0, -1, 1/2**0.5]
    VertCoord = [v0, v1, v2, v3]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def tetr_face_COM_coord(a: float, b: float, c: float):
    n = 10
    mid_a = mid_pt(b, c)
    mid_b = mid_pt(a, c)
    mid_c = mid_pt(a, b)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(30/180*math.pi)), 12))

    if COM_a == COM_b and COM_b == COM_c:
        return COM_a
    else:
        return COM_a


def tetr_face_COM_list_gen(radius: float):
    coord = tetr_face_coord(radius)
    COM_list = []
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[2]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[2], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[1], coord[2], coord[3]))
    return COM_list


def tetr_face_COM_leg_coord(a: float, b: float, c: float):
    COM_leg = []
    COM_leg.append(tetr_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


def tetr_face_COM_leg_list_gen(radius: float):
    coord = tetr_face_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[2]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[2], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[1], coord[2], coord[3]))
    return COM_leg_list


def tetr_face_leg_reduce(COM: float, leg: float, sigma: float):
    n = 12
    angle = math.acos(1/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def tetr_face_leg_reduce_coord_gen(radius: float, sigma: float):
    COM_leg_list = tetr_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def tetr_face_input_coord(radius: float, sigma: float):
    coor = tetr_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


def tetr_face_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = tetr_face_input_coord(radius, sigma)
    coord = tetr_face_leg_reduce_coord_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][1], coord[2][0], coord[2][1])

    f = open('parm.inp', 'w')
    f.write(' # Input file (tetrahedron face-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    tetr : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    tetr(lg1) + tetr(lg1) <-> tetr(lg1!1).tetr(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg2) <-> tetr(lg2!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg3) + tetr(lg3) <-> tetr(lg3!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg2) <-> tetr(lg1!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg3) <-> tetr(lg1!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg3) <-> tetr(lg2!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('tetr.mol', 'w')
    f.write('##\n')
    f.write('# Tetrahedron (face-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = tetr\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


# TETRAHEDRON VERTEX AS COM

def tetr_vert_coord(radius: float):
    scaler = radius/(3/8)**0.5/2
    v0 = [1, 0, -1/2**0.5]
    v1 = [-1, 0, -1/2**0.5]
    v2 = [0, 1, 1/2**0.5]
    v3 = [0, -1, 1/2**0.5]
    VertCoord = [v0, v1, v2, v3]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def tetr_vert_COM_leg(COM: float, a: float, b: float, c: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


def tetr_vert_COM_leg_gen(radius: float):
    coord = tetr_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[1], coord[2], coord[3], coord[0]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[2], coord[3], coord[0], coord[1]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[3], coord[0], coord[1], coord[2]))
    return COM_leg_list


def tetr_vert_leg_reduce(COM: float, leg: float, sigma: float):
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def tetr_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = tetr_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def tetr_vert_input_coord(radius: float, sigma: float):
    coor = tetr_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, n


def tetr_vert_norm_input(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = tetr_vert_input_coord(radius, sigma)
    length = distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


def tetr_vert_write(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = tetr_vert_norm_input(radius, sigma)
    f = open('parm.inp', 'w')
    f.write(' # Input file (tetrahedron vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    tetr : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    tetr(lg1) + tetr(lg1) <-> tetr(lg1!1).tetr(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg2) <-> tetr(lg2!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg3) + tetr(lg3) <-> tetr(lg3!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg2) <-> tetr(lg1!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg3) <-> tetr(lg1!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg3) <-> tetr(lg2!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('tetr.mol', 'w')
    f.write('##\n')
    f.write('# Tetrahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = tetr\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')


def tetr_face(radius: float, sigma: float):
    tetr_face_write(radius, sigma)
    print('File writing complete!')
    return 0


def cube_face(radius: float, sigma: float):
    cube_face_write(radius, sigma)
    print('File writing complete!')
    return 0


def octa_face(radius: float, sigma: float):
    octa_face_write(radius, sigma)
    print('File writing complete!')
    return 0


def dode_face(radius: float, sigma: float):
    dode_face_write(radius, sigma)
    print('File writing complete!')
    return 0


def icos_face(radius: float, sigma: float):
    icos_face_write(radius, sigma)
    print('File writing complete!')
    return 0


def tetr_vert(radius: float, sigma: float):
    tetr_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


def cube_vert(radius: float, sigma: float):
    cube_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


def octa_vert(radius: float, sigma: float):
    octa_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


def dode_vert(radius: float, sigma: float):
    dode_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


def icos_vert(radius: float, sigma: float):
    icos_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


# -----------------------------------Data Extraction--------------------------------

class data_type:
    def x(data:tuple):
        return data[0]
    def y(data:tuple):
        return data[1]
    def z(data:tuple):
        return data[2]
    def std(data:tuple):
        return data[3]

# -----------------------------------Data Visualization------------------------------

# Analysis tools for 'histogram_complexes_time.dat' file

def read_file(FileName: str, SpeciesName: str):
    hist = []
    hist_temp = []
    hist_conv = []
    hist_count = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:4] == 'Time':
                if hist_count != [] and hist_conv != []:
                    hist_temp.append(hist_count)
                    hist_temp.append(hist_conv)
                    hist.append(hist_temp)
                hist_count = []
                hist_conv = []
                hist_temp = []
                hist_temp.append(float(line.strip('Time (s): ')))
            else:
                string = '	' + str(SpeciesName) + ': '
                line = line.strip('. \n').split(string)
                if len(line) != 2:
                    print('Wrong species name!')
                    return 0
                else:
                    hist_count.append(int(line[0]))
                    hist_conv.append(int(line[1]))
            hist_temp.append(hist_count)
            hist_temp.append(hist_conv)
            hist.append(hist_temp)
    hist_ = []
    time_list = []
    for i in range(len(hist)):
        temp = []
        if hist[i][0] not in time_list:
            time_list.append(hist[i][0])
            temp = [hist[i][0], hist[i][1], hist[i][2]]
            hist_.append(temp)
    return hist_


def hist(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, BarSize: int = 1, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    count_list = []
    size_list = []
    for k in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(k) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_count_list = []
        hist = read_file(temp_file_name, SpeciesName)
        data_count = 0
        for i in hist:
            if InitialTime <= i[0] <= FinalTime:
                data_count += 1
                for j in i[2]:
                    if j not in total_size_list:
                        total_size_list.append(j)
                        total_count_list.append(i[1][i[2].index(j)])
                    else:
                        index = total_size_list.index(j)
                        total_count_list[index] += i[1][i[2].index(j)]
        total_count_list = np.array(total_count_list)/data_count
        if len(total_size_list) != 0:
            total_size_list_sorted = np.arange(1, max(total_size_list)+1, 1)
        else:
            total_size_list_sorted = np.array([])
        total_count_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_count_list_sorted.append(total_count_list[index])
            else:
                total_count_list_sorted.append(0.0)
        size_list.append(total_size_list_sorted)
        count_list.append(total_count_list_sorted)
    max_size = 0
    for i in size_list:
        if max_size < len(i):
            max_size = len(i)
            n_list = i
    count_list_filled = np.zeros([FileNum, max_size])
    for i in range(len(count_list)):
        for j in range(len(count_list[i])):
            count_list_filled[i][j] += count_list[i][j]
    count_list_rev = []
    for i in range(len(count_list_filled[0])):
        temp = []
        for j in range(len(count_list_filled)):
            temp.append(count_list_filled[j][i])
        count_list_rev.append(temp)
    mean = []
    std = []
    for i in count_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    mean_ = []
    std_ = []
    n_list_ = []
    temp_mean = 0
    temp_std = 0
    bar_size_count = 0
    for i in range(len(mean)):
        temp_mean += mean[i]
        temp_std += std[i]
        bar_size_count += 1
        if i+1 == len(mean):
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
        elif bar_size_count >= BarSize:
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
            temp_mean = 0
            temp_std = 0
            bar_size_count = 0
    mean_ = np.array(mean_)
    std_ = np.array(std_)
    n_list_ = np.array(n_list_)
    if FileNum != 1:
        plt.bar(n_list_, mean_, width=BarSize, color='C0',
                yerr=std_, ecolor='C1', capsize=2)
    else:
        plt.bar(n_list_, mean_, width=BarSize)
    plt.title('Histogram of ' + str(SpeciesName))
    plt.xlabel('# of ' + SpeciesName + ' in sigle complex')
    plt.ylabel('Count')
    if SaveFig:
        plt.savefig('Histogram.png', dpi=500)
    plt.show()
    return n_list_, mean_, 'Nan', std_


def max_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for k in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(k) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist = read_file(temp_file_name, SpeciesName)
        for i in hist:
            if InitialTime <= i[0] <= FinalTime:
                total_time_list.append(i[0])
                total_size_list.append(max(i[2]))
        time_list.append(total_time_list)
        size_list.append(total_size_list)

    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in range(len(size_list_rev)):
        mean.append(np.mean(size_list_rev[i]))
        if FileNum > 1:
            std.append(np.std(size_list_rev[i]))
    errorbar_color = '#c9e3f6'
    plt.plot(time_list[0], mean, color='C0')
    if FileNum > 1:
        plt.errorbar(time_list[0], mean, color='C0',
                     yerr=std, ecolor=errorbar_color)
    plt.title('Maximum Number of ' +
              str(SpeciesName) + ' in Single Complex')
    plt.xlabel('Time')
    plt.ylabel('Maximum Number of ' + str(SpeciesName))
    if SaveFig:
        plt.savefig('max_complex.png', dpi=500)
    plt.show()
    return time_list[0], mean, 'Nan', std


def mean_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, ExcludeSize: int = 0, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for k in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(k) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist = read_file(temp_file_name, SpeciesName)
        if ExcludeSize == 0:
            for i in hist:
                if InitialTime <= i[0] <= FinalTime:
                    total_time_list.append(i[0])
                    total_size_list.append(np.mean(i[2]))
        elif ExcludeSize > 0:
            for i in hist:
                if InitialTime <= i[0] <= FinalTime:
                    count = 1
                    N = 0
                    temp_sum = 0
                    total_time_list.append(i[0])
                    while count <= len(i[1]):
                        if i[2][count-1] >= ExcludeSize:
                            temp_sum += i[2][count-1]
                            N += 1
                        if count == len(i[1]):
                            if N != 0:
                                total_size_list.append(temp_sum/N)
                            else:
                                total_size_list.append(0)
                        count += 1
        else:
            print('ExcludeSize cannot smaller than 0!')
            return 0
        time_list.append(total_time_list)
        size_list.append(total_size_list)
    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in range(len(size_list_rev)):
        mean.append(np.mean(size_list_rev[i]))
        if FileNum > 1:
            std.append(np.std(size_list_rev[i]))
    errorbar_color = '#c9e3f6'
    plt.plot(time_list[0], mean, color='C0')
    if FileNum > 1:
        plt.errorbar(time_list[0], mean, color='C0',
                     yerr=std, ecolor=errorbar_color)
    plt.title('Average Number of ' +
              str(SpeciesName) + ' in Single Complex')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Number of ' + str(SpeciesName))
    if SaveFig:
        plt.savefig('mean_complex.png', dpi=500)
    plt.show()
    return time_list[0], mean, 'Nan', std


def single_hist_to_csv(FileName: str):
    name_list = ['Time (s)']
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:9] != 'Time (s):':
                name = line.split('	')[1].strip(' \n')
                name_num = int(line.split('	')[1].split(' ')[1].strip('.'))
                if name_list != ['Time (s)']:
                    last_num = int(name_list[-1].split(' ')[1].strip('.'))
                else:
                    last_num = 0
                if name not in name_list:
                    if name_num-last_num == 1:
                        name_list.append(name)
                    else:
                        fill = range(last_num+1, name_num)
                        for i in fill:
                            name = str(line.split('	')[1].split(
                                ' ')[0]) + ' ' + str(i) + '.'
                            name_list.append(name)
    file.close()
    with open(FileName, 'r') as read_file, open('histogram.csv', 'w') as write_file:
        head = ''
        for i in name_list:
            head += i
            if i != name_list[-1]:
                head += ','
            else:
                head += '\n'
        write_file.write(head)
        stat = np.zeros(len(name_list))
        for line in read_file.readlines():
            if line[0:9] == 'Time (s):':
                if line != 'Time (s): 0\n':
                    write_line = ''
                    for i in range(len(stat)):
                        write_line += str(stat[i])
                        if i != len(stat)-1:
                            write_line += ','
                        else:
                            write_line += '\n'
                    write_file.write(write_line)
                stat = np.zeros(len(name_list))
                write_line = ''
                info = float(line.split(' ')[-1])
                stat[0] += info
            else:
                name = line.split('	')[-1].strip(' \n')
                num = float(line.split('	')[0])
                index = name_list.index(name)
                stat[index] += num
        for i in range(len(stat)):
            write_line += str(stat[i])
            if i != len(stat)-1:
                write_line += ','
            else:
                write_line += '\n'
        write_file.write(write_line)
    read_file.close()
    write_file.close()
    return 0


def single_hist_to_df(FileName: str, SaveCsv: bool = True):
    single_hist_to_csv(FileName)
    df = pd.read_csv('histogram.csv')
    if not SaveCsv:
        os.remove('histogram.csv')
    return df


def multi_hist_to_csv(FileName: str):
    name_list = ['Time (s)']
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:9] != 'Time (s):':
                name = line.split('	')[1].strip(' \n')
                if name not in name_list:
                    name_list.append(name)
    file.close()
    with open(FileName, 'r') as read_file, open('histogram.csv', 'w') as write_file:
        head = ''
        for i in name_list:
            head += i
            if i != name_list[-1]:
                head += ','
            else:
                head += '\n'
        write_file.write(head)
        stat = np.zeros(len(name_list))
        for line in read_file.readlines():
            if line[0:9] == 'Time (s):':
                if line != 'Time (s): 0\n':
                    write_line = ''
                    for i in range(len(stat)):
                        write_line += str(stat[i])
                        if i != len(stat)-1:
                            write_line += ','
                        else:
                            write_line += '\n'
                    write_file.write(write_line)
                stat = np.zeros(len(name_list))
                write_line = ''
                info = float(line.split(' ')[-1])
                stat[0] += info
            else:
                name = line.split('	')[-1].strip(' \n')
                num = float(line.split('	')[0])
                index = name_list.index(name)
                stat[index] += num
        for i in range(len(stat)):
            write_line += str(stat[i])
            if i != len(stat)-1:
                write_line += ','
            else:
                write_line += '\n'
        write_file.write(write_line)
    read_file.close()
    write_file.close()
    return 0


def multi_hist_to_df(FileName: str, SaveCsv: bool = True):
    multi_hist_to_csv(FileName)
    df = pd.read_csv('histogram.csv')
    if not SaveCsv:
        os.remove('histogram.csv')
    return df


def hist_temp(FileName: str, InitialTime: float, FinalTime: float, SpeciesName: str):
    hist = read_file(FileName, SpeciesName)
    plot_count = []
    plot_conv = []
    tot = 0
    for i in hist:
        if InitialTime <= i[0] <= FinalTime:
            tot += 1
            for j in i[2]:
                if j not in plot_conv:
                    plot_conv.append(j)
                    plot_count.append(i[1][i[2].index(j)])
                else:
                    index = plot_conv.index(j)
                    plot_count[index] += i[1][i[2].index(j)]
    plot_count_mean = []
    for i in plot_count:
        plot_count_mean.append(i/tot)
    return plot_conv, plot_count_mean


def hist_3d_time(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, TimeBins: int, xBarSize: int = 1, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    z_list_tot = []
    x_list_tot = []
    for p in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(p) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        max_num = 0
        x_lst = []
        z_lst = []
        t_plt = np.zeros(TimeBins)
        i = 0
        for i in range(0, len(t_arr)-1):
            t_plt[i] = (t_arr[i]+t_arr[i+1])/2
            x, z = hist_temp(temp_file_name, t_arr[i], t_arr[i+1], SpeciesName)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        z_plt = np.zeros(shape=(max_num, TimeBins))
        k = 0
        for i in x_lst:
            l = 0
            for j in i:
                z_plt[j-1, k] = z_lst[k][l]
                l += 1
            k += 1
        z_plt = z_plt.T
        z_plt_ = []
        for i in range(len(z_plt)):
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            for j in range(len(z_plt[i])):
                x_count += 1
                sum_ += z_plt[i][j]
                if j == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    max_x_num = 0
    for i in range(len(x_list_tot)):
        if len(x_list_tot[i]) > max_x_num:
            max_x_num = len(x_list_tot[i])
            n_list = x_list_tot[i]
    for i in range(len(z_list_tot)):
        for j in range(len(z_list_tot[i])):
            if len(z_list_tot[i][j]) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(z_list_tot[i][j])):
                    z_list_tot[i][j] = np.append(z_list_tot[i][j], 0.0)
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
    xx, yy = np.meshgrid(n_list, t_plt)
    X, Y = xx.ravel(), yy.ravel()
    Z = np.array(count_list_mean.ravel())
    bottom = np.zeros_like(Z)
    width = xBarSize
    depth = 1/TimeBins
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.bar3d(X, Y, bottom, width, depth, Z, shade=True)
    ax.set_xlabel('# of ' + SpeciesName + ' in sigle complex')
    ax.set_ylabel('Time')
    ax.set_zlabel('Count')
    if SaveFig:
        plt.savefig('histogram_3D.png', dpi=500)
    plt.show()
    return n_list, t_plt, count_list_mean, 'Nan'


def hist_time_heatmap(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    z_list_tot = []
    x_list_tot = []
    for p in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(p) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        max_num = 0
        x_lst = []
        z_lst = []
        t_plt = []
        i = 0
        for i in range(0, len(t_arr)-1):
            t_plt.append(str(round(t_arr[i], 2)) +
                         's ~ ' + str(round(t_arr[i+1], 2)) + 's')
            x, z = hist_temp(temp_file_name, t_arr[i], t_arr[i+1], SpeciesName)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        z_plt = np.zeros(shape=(max_num, TimeBins))
        k = 0
        for i in x_lst:
            l = 0
            for j in i:
                z_plt[j-1, k] = z_lst[k][l]
                l += 1
            k += 1
        x_plt = np.arange(0, max_num, 1)+1
        z_plt = np.array(z_plt).T
        z_plt_ = []
        for i in range(len(z_plt)):
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            for j in range(len(z_plt[i])):
                x_count += 1
                sum_ += z_plt[i][j]
                if j == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    max_x_num = 0
    for i in range(len(x_list_tot)):
        if len(x_list_tot[i]) > max_x_num:
            max_x_num = len(x_list_tot[i])
            n_list = x_list_tot[i]
    for i in range(len(z_list_tot)):
        for j in range(len(z_list_tot[i])):
            if len(z_list_tot[i][j]) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(z_list_tot[i][j])):
                    z_list_tot[i][j] = np.append(z_list_tot[i][j], 0.0)
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    count_list_std = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    fig, ax = plt.subplots()
    im = ax.imshow(count_list_mean)
    ax.set_xticks(np.arange(len(n_list)))
    ax.set_yticks(np.arange(len(t_plt)))
    ax.set_xticklabels(n_list)
    ax.set_yticklabels(t_plt)
    if ShowMean and ShowStd:
        print('Cannot show both maen and std!')
        return 0
    if ShowMean:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_mean[i, j], 1), ha='center', va='center', color='w')
    elif ShowStd and FileNum != 1:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_std[i, j], 1), ha='center', va='center', color='w')
    ax.set_title('N-mers distribution vs. Time')
    fig.tight_layout()
    plt.colorbar(im)
    plt.xlabel('Size of N-mers')
    plt.ylabel('Time')
    if SaveFig:
        plt.savefig('hist_heatmap.png', dpi=500, bbox_inches='tight')
    plt.show()
    return n_list, t_plt, count_list_mean, count_list_std


def hist_time_heatmap_mono_count(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    z_list_tot = []
    x_list_tot = []
    for p in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(p) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        max_num = 0
        x_lst = []
        z_lst = []
        t_plt = []
        i = 0
        for i in range(0, len(t_arr)-1):
            t_plt.append(str(round(t_arr[i], 2)) +
                         's ~ ' + str(round(t_arr[i+1], 2)) + 's')
            x, z = hist_temp(temp_file_name, t_arr[i], t_arr[i+1], SpeciesName)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        z_plt = np.zeros(shape=(max_num, TimeBins))
        k = 0
        for i in x_lst:
            l = 0
            for j in i:
                z_plt[j-1, k] = z_lst[k][l]
                l += 1
            k += 1
        x_plt = np.arange(0, max_num, 1)+1
        const = 1
        z_plt_mod = []
        for i in z_plt:
            z_plt_mod_temp = []
            for j in i:
                z_plt_mod_temp.append(j * const)
            const += 1
            z_plt_mod.append(z_plt_mod_temp)
        z_plt = np.array(z_plt_mod).T
        z_plt_ = []
        for i in range(len(z_plt)):
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            for j in range(len(z_plt[i])):
                x_count += 1
                sum_ += z_plt[i][j]
                if j == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    max_x_num = 0
    for i in range(len(x_list_tot)):
        if len(x_list_tot[i]) > max_x_num:
            max_x_num = len(x_list_tot[i])
            n_list = x_list_tot[i]
    for i in range(len(z_list_tot)):
        for j in range(len(z_list_tot[i])):
            if len(z_list_tot[i][j]) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(z_list_tot[i][j])):
                    z_list_tot[i][j] = np.append(z_list_tot[i][j], 0.0)
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    count_list_std = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    fig, ax = plt.subplots()
    im = ax.imshow(count_list_mean)
    ax.set_xticks(np.arange(len(n_list)))
    ax.set_yticks(np.arange(len(t_plt)))
    ax.set_xticklabels(n_list)
    ax.set_yticklabels(t_plt)
    if ShowMean and ShowStd:
        print('Cannot show both maen and std!')
        return 0
    if ShowMean:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_mean[i, j], 1), ha='center', va='center', color='w')
    elif ShowStd and FileNum != 1:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_std[i, j], 1), ha='center', va='center', color='w')
    ax.set_title('Total Number of Monomers in Complexes  vs. Time')
    fig.tight_layout()
    plt.colorbar(im)
    plt.xlabel('Size of N-mers')
    plt.ylabel('Time')
    if SaveFig:
        plt.savefig('hist_heatmap_count.png', dpi=500, bbox_inches='tight')
    plt.show()
    return n_list, t_plt, count_list_mean, count_list_std


def hist_time_heatmap_fraction(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    z_list_tot = []
    x_list_tot = []
    for p in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(p) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        xx, zz = hist_temp(temp_file_name, 0, 0, SpeciesName)
        n_tot = sum(zz)
        max_num = 0
        x_lst = []
        z_lst = []
        t_plt = []
        i = 0
        for i in range(0, len(t_arr)-1):
            t_plt.append(str(round(t_arr[i], 2)) +
                         's ~ ' + str(round(t_arr[i+1], 2)) + 's')
            x, z = hist_temp(temp_file_name, t_arr[i], t_arr[i+1], SpeciesName)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        z_plt = np.zeros(shape=(max_num, TimeBins))
        k = 0
        for i in x_lst:
            l = 0
            for j in i:
                z_plt[j-1, k] = z_lst[k][l]
                l += 1
            k += 1
        x_plt = np.arange(0, max_num, 1)+1
        const = 1
        z_plt_mod = []
        for i in z_plt:
            z_plt_mod_temp = []
            for j in i:
                z_plt_mod_temp.append(j * const / n_tot)
            const += 1
            z_plt_mod.append(z_plt_mod_temp)
        z_plt = np.array(z_plt_mod).T
        z_plt_ = []
        for i in range(len(z_plt)):
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            for j in range(len(z_plt[i])):
                x_count += 1
                sum_ += z_plt[i][j]
                if j == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    max_x_num = 0
    for i in range(len(x_list_tot)):
        if len(x_list_tot[i]) > max_x_num:
            max_x_num = len(x_list_tot[i])
            n_list = x_list_tot[i]
    for i in range(len(z_list_tot)):
        for j in range(len(z_list_tot[i])):
            if len(z_list_tot[i][j]) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(z_list_tot[i][j])):
                    z_list_tot[i][j] = np.append(z_list_tot[i][j], 0.0)
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    count_list_std = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    fig, ax = plt.subplots()
    im = ax.imshow(count_list_mean)
    ax.set_xticks(np.arange(len(n_list)))
    ax.set_yticks(np.arange(len(t_plt)))
    ax.set_xticklabels(n_list)
    ax.set_yticklabels(t_plt)
    if ShowMean and ShowStd:
        print('Cannot show both maen and std!')
        return 0
    if ShowMean:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_mean[i, j], 1), ha='center', va='center', color='w')
    elif ShowStd and FileNum != 1:
        for i in range(len(t_plt)):
            for j in range(len(n_list)):
                text = ax.text(j, i, round(
                    count_list_std[i, j], 1), ha='center', va='center', color='w')
    ax.set_title('Franction of Monomers in Complexes vs. Time')
    fig.tight_layout()
    plt.colorbar(im)
    plt.xlabel('Size of N-mers')
    plt.ylabel('Time')
    if SaveFig:
        plt.savefig('hist_heatmap_fraction.png', dpi=500, bbox_inches='tight')
    plt.show()
    return n_list, t_plt, count_list_mean, count_list_std

# Analysing tools for 'transition_matrix_time.dat'


def read_transition_matrix(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    ti_switch = False
    tf_switch = False
    spec_switch = False
    ti_matrix = []
    tf_matrix = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:5] == 'time:':
                if float(line.split(' ')[1]) == InitialTime:
                    ti_switch = True
                if float(line.split(' ')[1]) == FinalTime:
                    tf_switch = True
                if float(line.split(' ')[1]) != InitialTime:
                    ti_switch = False
                if float(line.split(' ')[1]) != FinalTime:
                    tf_switch = False
            if line[0:8] == 'lifetime':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            if line[0:4] == 'size':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            if line[0:4] == SpeciesName:
                spec_switch = True
            if ti_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for i in info:
                        temp_list.append(int(i))
                    ti_matrix.append(temp_list)
            if tf_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for i in info:
                        temp_list.append(int(i))
                    tf_matrix.append(temp_list)
    ti_matrix = np.array(ti_matrix)
    tf_matrix = np.array(tf_matrix)
    return ti_matrix, tf_matrix


def free_energy(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    sum_list_list = []
    for k in range(len(matrix_list)):
        sum_list = np.zeros(len(matrix))
        i = 0
        while i < len(matrix_list[k]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i == j:
                    sum_list[i] += matrix_list[k][i][j]
                elif i > j:
                    if i % 2 == 0:
                        if j <= (i-1)/2:
                            sum_list[i] += matrix_list[k][i][j]
                    else:
                        if j <= i/2:
                            if (i-1)/2 == j:
                                sum_list[i] += matrix_list[k][i][j]/2
                            else:
                                sum_list[i] += matrix_list[k][i][j]
                else:
                    if j % 2 != 0:
                        if i <= j/2:
                            if (j-1)/2 == i:
                                sum_list[i] += matrix_list[k][i][j]/2
                            else:
                                sum_list[i] += matrix_list[k][i][j]
                        else:
                            sum_list[i] += matrix_list[k][i][j]
                    else:
                        sum_list[i] += matrix_list[k][i][j]
                j += 1
            i += 1
        sum_list_list.append(sum_list)
    energy_list_list = []
    for i in range(len(sum_list_list)):
        sum_arr = np.array(sum_list_list[i])
        sum_arr = sum_arr/sum_arr.sum()
        energy_list = np.asarray([])
        for i in sum_arr:
            if i > 0:
                energy_list = np.append(energy_list, -math.log(i))
            else:
                energy_list = np.append(energy_list, np.nan)
        energy_list_list.append(energy_list)
    n_list = list(range(1, 1 + len(matrix_list[0])))
    energy_list_list_rev = []
    for i in range(len(energy_list_list[0])):
        temp = []
        for j in range(len(energy_list_list)):
            temp.append(energy_list_list[j][i])
        energy_list_list_rev.append(temp)
    mean_energy_list = np.array([])
    std_energy_list = np.array([])
    for i in energy_list_list_rev:
        mean_energy_list = np.append(mean_energy_list, np.nanmean(i))
        if FileNum != 1:
            std_energy_list = np.append(std_energy_list, np.nanstd(i))
    errorbar_color = '#c9e3f6'
    plt.plot(n_list, mean_energy_list, 'C0')
    if FileNum != 1:
        plt.errorbar(n_list, mean_energy_list, yerr=std_energy_list,
                     ecolor=errorbar_color, capsize=2)
    plt.title('Free Energy Vs. Time from ' + str(float(InitialTime)
                                                 ) + 's to ' + str(float(FinalTime)) + 's')
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('-ln(p(N)) ($k_B$T)')
    plt.xticks(ticks=n_list)
    if SaveFig:
        plt.savefig('free_energy.png', dpi=500)
    plt.show()
    return n_list, mean_energy_list, 'Nan', std_energy_list


def associate_prob_symmetric(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, DivideSize: int = 2, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    above = []
    equal = []
    below = []
    for k in range(len(matrix_list)):
        above_temp = np.zeros(len(matrix_list[0][0]))
        equal_temp = np.zeros(len(matrix_list[0][0]))
        below_temp = np.zeros(len(matrix_list[0][0]))
        i = 0
        while i < len(matrix_list[k]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i > j:
                    if i - j == DivideSize:
                        equal_temp[j] += matrix_list[k][i][j]
                    elif i - j > DivideSize:
                        above_temp[j] += matrix_list[k][i][j]
                    else:
                        below_temp[j] += matrix_list[k][i][j]
                j += 1
            i += 1
        above.append(above_temp)
        equal.append(equal_temp)
        below.append(below_temp)
    above_prob = []
    equal_prob = []
    below_prob = []
    for i in range(len(above)):
        above_prob_temp = np.array([])
        equal_prob_temp = np.array([])
        below_prob_temp = np.array([])
        for j in range(len(above[0])):
            sum = above[i][j] + equal[i][j] + below[i][j]
            if sum != 0:
                above_prob_temp = np.append(above_prob_temp, above[i][j]/sum)
                equal_prob_temp = np.append(equal_prob_temp, equal[i][j]/sum)
                below_prob_temp = np.append(below_prob_temp, below[i][j]/sum)
            else:
                above_prob_temp = np.append(above_prob_temp, np.nan)
                equal_prob_temp = np.append(equal_prob_temp, np.nan)
                below_prob_temp = np.append(below_prob_temp, np.nan)
        above_prob.append(above_prob_temp)
        equal_prob.append(equal_prob_temp)
        below_prob.append(below_prob_temp)
    above_prob_rev = []
    for i in range(len(above_prob[0])):
        temp = []
        for j in range(len(above_prob)):
            temp.append(above_prob[j][i])
        above_prob_rev.append(temp)
    equal_prob_rev = []
    for i in range(len(equal_prob[0])):
        temp = []
        for j in range(len(equal_prob)):
            temp.append(equal_prob[j][i])
        equal_prob_rev.append(temp)
    below_prob_rev = []
    for i in range(len(below_prob[0])):
        temp = []
        for j in range(len(below_prob)):
            temp.append(below_prob[j][i])
        below_prob_rev.append(temp)
    mean_above = []
    mean_equal = []
    mean_below = []
    std_above = []
    std_equal = []
    std_below = []
    for i in range(len(above_prob_rev)):
        mean_above.append(np.nanmean(above_prob_rev[i]))
        mean_equal.append(np.nanmean(equal_prob_rev[i]))
        mean_below.append(np.nanmean(below_prob_rev[i]))
        if FileNum != 1:
            std_above.append(np.nanstd(above_prob_rev[i]))
            std_equal.append(np.nanstd(equal_prob_rev[i]))
            std_below.append(np.nanstd(below_prob_rev[i]))
    n_list = list(range(1, 1 + len(matrix_list[0])))
    errorbar_color_1 = '#c9e3f6'
    errorbar_color_2 = '#ffe7d2'
    errorbar_color_3 = '#d7f4d7'
    plt.plot(n_list, mean_above, 'C0')
    plt.plot(n_list, mean_equal, 'C1')
    plt.plot(n_list, mean_below, 'C2')
    if FileNum != 1:
        plt.errorbar(n_list, mean_above, yerr=std_above,
                     ecolor=errorbar_color_1, capsize=2)
        plt.errorbar(n_list, mean_equal, yerr=std_equal,
                     ecolor=errorbar_color_2, capsize=2)
        plt.errorbar(n_list, mean_below, yerr=std_below,
                     ecolor=errorbar_color_3, capsize=2)
    plt.legend(['Associate Size > ' + str(DivideSize), 'Associate Size = ' +
               str(DivideSize), 'Associate Size < ' + str(DivideSize)])
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('Probability')
    plt.xticks(ticks=n_list)
    plt.title('Remodeling of Complex')
    if SaveFig:
        plt.savefig('associate_probability_symmetric.png', dpi=500)
    plt.show()
    return n_list, [mean_above, mean_equal, mean_below], 'Nan', [std_above, std_equal, std_below]


def associate_prob_asymmetric(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, DivideSize: int = 2, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    above = []
    equal = []
    below = []
    for k in range(len(matrix_list)):
        above_temp = np.zeros(len(matrix_list[0][0]))
        equal_temp = np.zeros(len(matrix_list[0][0]))
        below_temp = np.zeros(len(matrix_list[0][0]))
        i = 0
        while i < len(matrix_list[k]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i > j:
                    if i % 2 == 0:
                        if j >= (i-1)/2:
                            if i - j == DivideSize:
                                equal_temp[j] += matrix_list[k][i][j]
                            elif i - j > DivideSize:
                                above_temp[j] += matrix_list[k][i][j]
                            else:
                                below_temp[j] += matrix_list[k][i][j]
                    else:
                        if j >= int(i/2):
                            if (i-1)/2 == j:
                                if i - j == DivideSize:
                                    equal_temp[j] += matrix_list[k][i][j]/2
                                elif i - j > DivideSize:
                                    above_temp[j] += matrix_list[k][i][j]/2
                                else:
                                    below_temp[j] += matrix_list[k][i][j]/2
                            else:
                                if i - j == DivideSize:
                                    equal_temp[j] += matrix_list[k][i][j]
                                elif i - j > DivideSize:
                                    above_temp[j] += matrix_list[k][i][j]
                                else:
                                    below_temp[j] += matrix_list[k][i][j]
                j += 1
            i += 1
        above.append(above_temp)
        equal.append(equal_temp)
        below.append(below_temp)
    above_prob = []
    equal_prob = []
    below_prob = []
    for i in range(len(above)):
        above_prob_temp = np.array([])
        equal_prob_temp = np.array([])
        below_prob_temp = np.array([])
        for j in range(len(above[0])):
            sum = above[i][j] + equal[i][j] + below[i][j]
            if sum != 0:
                above_prob_temp = np.append(above_prob_temp, above[i][j]/sum)
                equal_prob_temp = np.append(equal_prob_temp, equal[i][j]/sum)
                below_prob_temp = np.append(below_prob_temp, below[i][j]/sum)
            else:
                above_prob_temp = np.append(above_prob_temp, np.nan)
                equal_prob_temp = np.append(equal_prob_temp, np.nan)
                below_prob_temp = np.append(below_prob_temp, np.nan)
        above_prob.append(above_prob_temp)
        equal_prob.append(equal_prob_temp)
        below_prob.append(below_prob_temp)
    above_prob_rev = []
    for i in range(len(above_prob[0])):
        temp = []
        for j in range(len(above_prob)):
            temp.append(above_prob[j][i])
        above_prob_rev.append(temp)
    equal_prob_rev = []
    for i in range(len(equal_prob[0])):
        temp = []
        for j in range(len(equal_prob)):
            temp.append(equal_prob[j][i])
        equal_prob_rev.append(temp)
    below_prob_rev = []
    for i in range(len(below_prob[0])):
        temp = []
        for j in range(len(below_prob)):
            temp.append(below_prob[j][i])
        below_prob_rev.append(temp)
    mean_above = []
    mean_equal = []
    mean_below = []
    std_above = []
    std_equal = []
    std_below = []
    for i in range(len(above_prob_rev)):
        mean_above.append(np.nanmean(above_prob_rev[i]))
        mean_equal.append(np.nanmean(equal_prob_rev[i]))
        mean_below.append(np.nanmean(below_prob_rev[i]))
        if FileNum != 1:
            std_above.append(np.nanstd(above_prob_rev[i]))
            std_equal.append(np.nanstd(equal_prob_rev[i]))
            std_below.append(np.nanstd(below_prob_rev[i]))
    n_list = list(range(1, 1 + len(matrix_list[0])))
    errorbar_color_1 = '#c9e3f6'
    errorbar_color_2 = '#ffe7d2'
    errorbar_color_3 = '#d7f4d7'
    plt.plot(n_list, mean_above, 'C0')
    plt.plot(n_list, mean_equal, 'C1')
    plt.plot(n_list, mean_below, 'C2')
    if FileNum != 1:
        plt.errorbar(n_list, mean_above, yerr=std_above,
                     ecolor=errorbar_color_1, capsize=2)
        plt.errorbar(n_list, mean_equal, yerr=std_equal,
                     ecolor=errorbar_color_2, capsize=2)
        plt.errorbar(n_list, mean_below, yerr=std_below,
                     ecolor=errorbar_color_3, capsize=2)
    plt.legend(['Associate Size > ' + str(DivideSize), 'Associate Size = ' +
               str(DivideSize), 'Associate Size < ' + str(DivideSize)])
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('Probability')
    plt.xticks(ticks=n_list)
    plt.title('Remodeling of Complex')
    if SaveFig:
        plt.savefig('associate_probability_asymmetric.png', dpi=500)
    plt.show()
    return n_list, [mean_above, mean_equal, mean_below], 'Nan', [std_above, std_equal, std_below]


def dissociate_prob_symmetric(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, DivideSize: int = 2, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    above = []
    equal = []
    below = []
    for k in range(len(matrix_list)):
        above_temp = np.zeros(len(matrix_list[0][0]))
        equal_temp = np.zeros(len(matrix_list[0][0]))
        below_temp = np.zeros(len(matrix_list[0][0]))
        i = 0
        while i < len(matrix_list[k][0]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i > j:
                    if j + 1 == DivideSize:
                        equal_temp[i] += matrix_list[k][j][i]
                    elif j + 1 > DivideSize:
                        above_temp[i] += matrix_list[k][j][i]
                    else:
                        below_temp[i] += matrix_list[k][j][i]
                j += 1
            i += 1
        above.append(above_temp)
        equal.append(equal_temp)
        below.append(below_temp)
    above_prob = []
    equal_prob = []
    below_prob = []
    for i in range(len(above)):
        above_prob_temp = np.array([])
        equal_prob_temp = np.array([])
        below_prob_temp = np.array([])
        for j in range(len(above[0])):
            sum = above[i][j] + equal[i][j] + below[i][j]
            if sum != 0:
                above_prob_temp = np.append(above_prob_temp, above[i][j]/sum)
                equal_prob_temp = np.append(equal_prob_temp, equal[i][j]/sum)
                below_prob_temp = np.append(below_prob_temp, below[i][j]/sum)
            else:
                above_prob_temp = np.append(above_prob_temp, np.nan)
                equal_prob_temp = np.append(equal_prob_temp, np.nan)
                below_prob_temp = np.append(below_prob_temp, np.nan)
        above_prob.append(above_prob_temp)
        equal_prob.append(equal_prob_temp)
        below_prob.append(below_prob_temp)
    above_prob_rev = []
    for i in range(len(above_prob[0])):
        temp = []
        for j in range(len(above_prob)):
            temp.append(above_prob[j][i])
        above_prob_rev.append(temp)
    equal_prob_rev = []
    for i in range(len(equal_prob[0])):
        temp = []
        for j in range(len(equal_prob)):
            temp.append(equal_prob[j][i])
        equal_prob_rev.append(temp)
    below_prob_rev = []
    for i in range(len(below_prob[0])):
        temp = []
        for j in range(len(below_prob)):
            temp.append(below_prob[j][i])
        below_prob_rev.append(temp)
    mean_above = []
    mean_equal = []
    mean_below = []
    std_above = []
    std_equal = []
    std_below = []
    for i in range(len(above_prob_rev)):
        mean_above.append(np.nanmean(above_prob_rev[i]))
        mean_equal.append(np.nanmean(equal_prob_rev[i]))
        mean_below.append(np.nanmean(below_prob_rev[i]))
        if FileNum != 1:
            std_above.append(np.nanstd(above_prob_rev[i]))
            std_equal.append(np.nanstd(equal_prob_rev[i]))
            std_below.append(np.nanstd(below_prob_rev[i]))
    mean_above = np.nan_to_num(mean_above)
    mean_equal = np.nan_to_num(mean_equal)
    mean_below = np.nan_to_num(mean_below)
    n_list = list(range(1, 1 + len(matrix_list[0])))
    errorbar_color_1 = '#c9e3f6'
    errorbar_color_2 = '#ffe7d2'
    errorbar_color_3 = '#d7f4d7'
    plt.plot(n_list, mean_above, 'C0')
    plt.plot(n_list, mean_equal, 'C1')
    plt.plot(n_list, mean_below, 'C2')
    if FileNum != 1:
        plt.errorbar(n_list, mean_above, yerr=std_above,
                     ecolor=errorbar_color_1, capsize=2)
        plt.errorbar(n_list, mean_equal, yerr=std_equal,
                     ecolor=errorbar_color_2, capsize=2)
        plt.errorbar(n_list, mean_below, yerr=std_below,
                     ecolor=errorbar_color_3, capsize=2)
    plt.legend(['Dissociate Size > ' + str(DivideSize), 'Dissociate Size = ' +
               str(DivideSize), 'Dissociate Size < ' + str(DivideSize)])
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('Probability')
    plt.xticks(ticks=n_list)
    plt.title('Remodeling of Complex')
    if SaveFig:
        plt.savefig('dissociate_probability_symmetric.png', dpi=500)
    plt.show()
    return n_list, [mean_above, mean_equal, mean_below], 'Nan', [std_above, std_equal, std_below]


def dissociate_prob_asymmetric(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, DivideSize: int = 2, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    above = []
    equal = []
    below = []
    for k in range(len(matrix_list)):
        above_temp = np.zeros(len(matrix_list[0][0]))
        equal_temp = np.zeros(len(matrix_list[0][0]))
        below_temp = np.zeros(len(matrix_list[0][0]))
        i = 0
        while i < len(matrix_list[k][0]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i > j:
                    if i % 2 == 0:
                        if j <= (i-1)/2:
                            if j + 1 == DivideSize:
                                equal_temp[i] += matrix_list[k][j][i]
                            elif j + 1 > DivideSize:
                                above_temp[i] += matrix_list[k][j][i]
                            else:
                                below_temp[i] += matrix_list[k][j][i]
                    else:
                        if j <= int(i/2):
                            if (i-1)/2 == j:
                                if j + 1 == DivideSize:
                                    equal_temp[i] += matrix_list[k][j][i]/2
                                elif j + 1 > DivideSize:
                                    above_temp[i] += matrix_list[k][j][i]/2
                                else:
                                    below_temp[i] += matrix_list[k][j][i]/2
                            else:
                                if j + 1 == DivideSize:
                                    equal_temp[i] += matrix_list[k][j][i]
                                elif j + 1 > DivideSize:
                                    above_temp[i] += matrix_list[k][j][i]
                                else:
                                    below_temp[i] += matrix_list[k][j][i]
                j += 1
            i += 1
        above.append(above_temp)
        equal.append(equal_temp)
        below.append(below_temp)
    above_prob = []
    equal_prob = []
    below_prob = []
    for i in range(len(above)):
        above_prob_temp = np.array([])
        equal_prob_temp = np.array([])
        below_prob_temp = np.array([])
        for j in range(len(above[0])):
            sum = above[i][j] + equal[i][j] + below[i][j]
            if sum != 0:
                above_prob_temp = np.append(above_prob_temp, above[i][j]/sum)
                equal_prob_temp = np.append(equal_prob_temp, equal[i][j]/sum)
                below_prob_temp = np.append(below_prob_temp, below[i][j]/sum)
            else:
                above_prob_temp = np.append(above_prob_temp, np.nan)
                equal_prob_temp = np.append(equal_prob_temp, np.nan)
                below_prob_temp = np.append(below_prob_temp, np.nan)
        above_prob.append(above_prob_temp)
        equal_prob.append(equal_prob_temp)
        below_prob.append(below_prob_temp)
    above_prob_rev = []
    for i in range(len(above_prob[0])):
        temp = []
        for j in range(len(above_prob)):
            temp.append(above_prob[j][i])
        above_prob_rev.append(temp)
    equal_prob_rev = []
    for i in range(len(equal_prob[0])):
        temp = []
        for j in range(len(equal_prob)):
            temp.append(equal_prob[j][i])
        equal_prob_rev.append(temp)
    below_prob_rev = []
    for i in range(len(below_prob[0])):
        temp = []
        for j in range(len(below_prob)):
            temp.append(below_prob[j][i])
        below_prob_rev.append(temp)
    mean_above = []
    mean_equal = []
    mean_below = []
    std_above = []
    std_equal = []
    std_below = []
    for i in range(len(above_prob_rev)):
        mean_above.append(np.nanmean(above_prob_rev[i]))
        mean_equal.append(np.nanmean(equal_prob_rev[i]))
        mean_below.append(np.nanmean(below_prob_rev[i]))
        if FileNum != 1:
            std_above.append(np.nanstd(above_prob_rev[i]))
            std_equal.append(np.nanstd(equal_prob_rev[i]))
            std_below.append(np.nanstd(below_prob_rev[i]))
    mean_above = np.nan_to_num(mean_above)
    mean_equal = np.nan_to_num(mean_equal)
    mean_below = np.nan_to_num(mean_below)
    n_list = list(range(1, 1 + len(matrix_list[0])))
    errorbar_color_1 = '#c9e3f6'
    errorbar_color_2 = '#ffe7d2'
    errorbar_color_3 = '#d7f4d7'
    plt.plot(n_list, mean_above, 'C0')
    plt.plot(n_list, mean_equal, 'C1')
    plt.plot(n_list, mean_below, 'C2')
    if FileNum != 1:
        plt.errorbar(n_list, mean_above, yerr=std_above,
                     ecolor=errorbar_color_1, capsize=2)
        plt.errorbar(n_list, mean_equal, yerr=std_equal,
                     ecolor=errorbar_color_2, capsize=2)
        plt.errorbar(n_list, mean_below, yerr=std_below,
                     ecolor=errorbar_color_3, capsize=2)
    plt.legend(['Dissociate Size > ' + str(DivideSize), 'Dissociate Size = ' +
               str(DivideSize), 'Dissociate Size < ' + str(DivideSize)])
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('Probability')
    plt.xticks(ticks=n_list)
    plt.title('Remodeling of Complex')
    if SaveFig:
        plt.savefig('dissociate_probability_asymmetric.png', dpi=500)
    plt.show()
    return n_list, [mean_above, mean_equal, mean_below], 'Nan', [std_above, std_equal, std_below]


def growth_prob(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    growth_list_list = []
    tot_list_list = []
    for k in range(len(matrix_list)):
        growth_list = []
        tot_list = []
        i = 0
        while i < len(matrix_list[k][0]):
            j = 0
            growth_sum = 0
            tot_sum = 0
            while j < len(matrix_list[k][i]):
                if i != j:
                    tot_sum += matrix_list[k][j][i]
                    if i < j:
                        growth_sum += matrix_list[k][j][i]
                j += 1
            growth_list.append(growth_sum)
            tot_list.append(tot_sum)
            i += 1
        growth_list_list.append(growth_list)
        tot_list_list.append(tot_list)
    growth_prob = []
    for i in range(len(growth_list_list)):
        growth_prob_temp = []
        for j in range(len(growth_list_list[i])):
            if tot_list_list[i][j] != 0:
                growth_prob_temp.append(
                    growth_list_list[i][j]/tot_list_list[i][j])
            else:
                growth_prob_temp.append(0.0)
        growth_prob.append(growth_prob_temp)
    growth_prob_rev = []
    for i in range(len(growth_prob[0])):
        temp = []
        for j in range(len(growth_prob)):
            temp.append(growth_prob[j][i])
        growth_prob_rev.append(temp)
    mean = []
    std = []
    for i in growth_prob_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    n_list = list(range(1, 1 + len(matrix_list[0])))
    errorbar_color = '#c9e3f6'
    plt.plot(n_list, mean, color='C0')
    if FileNum != 1:
        plt.errorbar(n_list, mean, yerr=std, ecolor=errorbar_color, capsize=2)
    plt.axhline(y=1/2, c='black', lw=1.0)
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('$P_{growth}$')
    plt.xticks(ticks=n_list)
    plt.yticks((0, 0.25, 0.5, 0.75, 1))
    plt.title('Growth Probability')
    if SaveFig:
        plt.savefig('growth_probability.png', dpi=500)
    plt.show()
    return n_list, mean, 'Nan', std


def read_cluster_lifetime(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    ti_switch = False
    tf_switch = False
    spec_switch = False
    lifetime_switch = False
    size_list = []
    ti_lifetime = []
    tf_lifetime = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:6] == 'time: ':
                lifetime_switch = False
                spec_switch = False
                if float(line.split(' ')[1].strip('\n')) == InitialTime:
                    ti_switch = True
                if float(line.split(' ')[1].strip('\n')) == FinalTime:
                    tf_switch = True
                if float(line.split(' ')[1].strip('\n')) != InitialTime:
                    ti_switch = False
                if float(line.split(' ')[1].strip('\n')) != FinalTime:
                    tf_switch = False
            if line == 'lifetime for each mol type: \n':
                lifetime_switch = True
            if line == str(SpeciesName) + '\n':
                spec_switch = True
            if ti_switch and lifetime_switch and spec_switch:
                if line != str(SpeciesName) + '\n' and line != 'lifetime for each mol type: \n':
                    if line[0:20] == 'size of the cluster:':
                        size_list.append(int(line.split(':')[1].strip('\n')))
                    else:
                        str_list = line.strip('\n').strip(' ').split(' ')
                        temp = np.array([])
                        for i in str_list:
                            if i != '':
                                temp = np.append(temp, float(i))
                        ti_lifetime.append(temp)
            if tf_switch and lifetime_switch and spec_switch:
                if line != str(SpeciesName) + '\n' and line != 'lifetime for each mol type: \n':
                    if line[0:20] != 'size of the cluster:':
                        str_list = line.strip('\n').strip(' ').split(' ')
                        temp = np.array([])
                        for i in str_list:
                            if i != '':
                                temp = np.append(temp, float(i))
                        tf_lifetime.append(temp)
    return ti_lifetime, tf_lifetime, size_list


def complex_lifetime(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesName: str, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    mean_lifetime = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_lifetime, tf_lifetime, size_list = read_cluster_lifetime(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        mean_temp = []
        for i in range(len(tf_lifetime)):
            tf_lifetime[i] = np.delete(
                tf_lifetime[i], range(0, len(ti_lifetime[i])), axis=0)
            mean_temp.append(tf_lifetime[i].mean())
        mean_lifetime.append(mean_temp)
    mean_lifetime_rev = []
    for i in range(len(mean_lifetime[0])):
        temp = []
        for j in range(len(mean_lifetime)):
            temp.append(mean_lifetime[j][i])
        mean_lifetime_rev.append(temp)
    mean = []
    std = []
    for i in mean_lifetime_rev:
        mean.append(np.nanmean(i))
        if FileNum != 1:
            std.append(np.nanstd(i))
    errorbar_color = '#c9e3f6'
    plt.plot(size_list, mean, color='C0')
    if FileNum != 1:
        plt.errorbar(size_list, mean, yerr=std,
                     ecolor=errorbar_color, capsize=2)
    plt.xlabel('N (copies of ' + str(SpeciesName) + ')')
    plt.ylabel('Lifetime (s)')
    plt.xticks(ticks=size_list)
    plt.title('Lifetime of Complex')
    if SaveFig:
        plt.savefig('complex_lifetime.png', dpi=500)
    plt.show()
    return size_list, mean, 'Nan', std


def read_multi_hist(FileName: str, SpeciesList: list):
    SpeciesList = np.array(SpeciesList)
    hist_list = []
    time_temp = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:10] == 'Time (s): ':
                if float(line.split(' ')[-1].strip('\n')) != 0:
                    hist_list.append(time_temp)
                time_temp = []
                time_temp.append(float(line.split(' ')[-1].strip('\n')))
            else:
                complex_temp = np.zeros(len(SpeciesList) + 1)
                count = int(line.split('	')[0])
                info = line.strip('. \n').split('	')[1].split('. ')
                for i in range(len(info)):
                    name = str(info[i].split(': ')[0])
                    num = int(info[i].split(': ')[1])
                    index = np.where(SpeciesList == name)[0][0]
                    complex_temp[index] += num
                complex_temp[-1] += count
                time_temp.append(complex_temp)
        hist_list.append(time_temp)
    return hist_list


def multi_hist(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
               SpeciesList: list, xAxis: str, BarSize: int = 1, ExcludeSize: int = 0,
               SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    count_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_count_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis == 'tot':
                                total_size = sum(hist_list[j][k][0:-1])
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        total_count_list.append(
                                            hist_list[j][k][-1])
                                    else:
                                        index = total_size_list.index(
                                            total_size)
                                        total_count_list[index] += hist_list[j][k][-1]
                            elif xAxis in SpeciesList:
                                name_index = SpeciesList.index(xAxis)
                                total_size = hist_list[j][k][name_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        total_count_list.append(
                                            hist_list[j][k][-1])
                                    else:
                                        index = total_size_list.index(
                                            total_size)
                                        total_count_list[index] += hist_list[j][k][-1]
                            else:
                                print('xAxis not in SpeciesList!')
                                return 0
        total_count_list = np.array(total_count_list)/data_count
        if len(total_size_list) != 0:
            total_size_list_sorted = np.arange(1, max(total_size_list)+1, 1)
        else:
            total_size_list_sorted = np.array([])
        total_count_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_count_list_sorted.append(total_count_list[index])
            else:
                total_count_list_sorted.append(0.0)
        size_list.append(total_size_list_sorted)
        count_list.append(total_count_list_sorted)
    max_size = 0
    for i in size_list:
        if max_size < len(i):
            max_size = len(i)
            n_list = i
    count_list_filled = np.zeros([FileNum, max_size])
    count_list_arr = np.array([])
    for i in range(len(count_list)):
        for j in range(len(count_list[i])):
            count_list_filled[i][j] += count_list[i][j]
    count_list_rev = []
    for i in range(len(count_list_filled[0])):
        temp = []
        for j in range(len(count_list_filled)):
            temp.append(count_list_filled[j][i])
        count_list_rev.append(temp)
    mean = []
    std = []
    for i in count_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))

    mean_ = []
    std_ = []
    n_list_ = []
    temp_mean = 0
    temp_std = 0
    bar_size_count = 0
    for i in range(len(mean)):
        temp_mean += mean[i]
        temp_std += std[i]
        bar_size_count += 1
        if i+1 == len(mean):
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
        elif bar_size_count >= BarSize:
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
            temp_mean = 0
            temp_std = 0
            bar_size_count = 0
    mean_ = np.array(mean_)
    std_ = np.array(std_)
    n_list_ = np.array(n_list_)

    if FileNum != 1:
        plt.bar(n_list_, mean_, width=BarSize, color='C0',
                yerr=std_, ecolor='C1', capsize=2)
    else:
        plt.bar(n_list_, mean_, width=BarSize)
    if xAxis == 'tot':
        label_name = 'total monomers'
    else:
        label_name = xAxis
    plt.xlabel('# of ' + label_name + ' in sigle complex (count)')
    plt.ylabel('Count')
    plt.title('Histogram of Multi-component Assemblies')
    fig_species = xAxis
    if xAxis == 'tot':
        fig_species = 'total_components'
    fig_name = 'histogram_of_' + fig_species
    if SaveFig:
        plt.savefig(fig_name, dpi=500)
    plt.show()
    return n_list_, mean_, 'Nan', std_


def multi_hist_stacked(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                       SpeciesList: list, xAxis: str, DivideSpecies: str, DivideSize: int,
                       BarSize: int = 1, ExcludeSize: int = 0, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    above_list = []
    equal_list = []
    below_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_above_list = []
        total_equal_list = []
        total_below_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis == 'tot' and DivideSpecies in SpeciesList:
                                total_size = sum(hist_list[j][k][0:-1])
                                divide_index = SpeciesList.index(DivideSpecies)
                                divide_spe_size = hist_list[j][k][divide_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        if divide_spe_size > DivideSize:
                                            total_above_list.append(
                                                hist_list[j][k][-1])
                                            total_equal_list.append(0.0)
                                            total_below_list.append(0.0)
                                        elif divide_spe_size == DivideSize:
                                            total_equal_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_below_list.append(0.0)
                                        else:
                                            total_below_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_equal_list.append(0.0)
                                    else:
                                        if divide_spe_size > DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_above_list[index] += hist_list[j][k][-1]
                                        elif divide_spe_size == DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_equal_list[index] += hist_list[j][k][-1]
                                        else:
                                            index = total_size_list.index(
                                                total_size)
                                            total_below_list[index] += hist_list[j][k][-1]
                            elif xAxis in SpeciesList and DivideSpecies in SpeciesList:
                                name_index = SpeciesList.index(xAxis)
                                total_size = hist_list[j][k][name_index]
                                divide_index = SpeciesList.index(DivideSpecies)
                                divide_spe_size = hist_list[j][k][divide_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        if divide_spe_size > DivideSize:
                                            total_above_list.append(
                                                hist_list[j][k][-1])
                                            total_equal_list.append(0.0)
                                            total_below_list.append(0.0)
                                        elif divide_spe_size == DivideSize:
                                            total_equal_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_below_list.append(0.0)
                                        else:
                                            total_below_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_equal_list.append(0.0)
                                    else:
                                        if divide_spe_size > DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_above_list[index] += hist_list[j][k][-1]
                                        elif divide_spe_size == DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_equal_list[index] += hist_list[j][k][-1]
                                        else:
                                            index = total_size_list.index(
                                                total_size)
                                            total_below_list[index] += hist_list[j][k][-1]
                            else:
                                print('xAxis or DivideSpecies not in SpeciesList!')
                                return 0
        total_above_list = np.array(total_above_list)/data_count
        total_equal_list = np.array(total_equal_list)/data_count
        total_below_list = np.array(total_below_list)/data_count
        if len(total_size_list) != 0:
            total_size_list_sorted = np.arange(1, max(total_size_list)+1, 1)
        else:
            total_size_list_sorted = np.array([])
        total_above_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_above_list_sorted.append(total_above_list[index])
            else:
                total_above_list_sorted.append(0.0)
        total_equal_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_equal_list_sorted.append(total_equal_list[index])
            else:
                total_equal_list_sorted.append(0.0)
        total_below_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_below_list_sorted.append(total_below_list[index])
            else:
                total_below_list_sorted.append(0.0)
        size_list.append(total_size_list_sorted)
        above_list.append(total_above_list_sorted)
        equal_list.append(total_equal_list_sorted)
        below_list.append(total_below_list_sorted)
    max_size = 0
    for i in size_list:
        if max_size < len(i):
            max_size = len(i)
            n_list = i
    above_list_filled = np.zeros([FileNum, max_size])
    above_list_arr = np.array([])
    for i in range(len(above_list)):
        for j in range(len(above_list[i])):
            above_list_filled[i][j] += above_list[i][j]
    equal_list_filled = np.zeros([FileNum, max_size])
    equal_list_arr = np.array([])
    for i in range(len(equal_list)):
        for j in range(len(equal_list[i])):
            equal_list_filled[i][j] += equal_list[i][j]
    below_list_filled = np.zeros([FileNum, max_size])
    below_list_arr = np.array([])
    for i in range(len(below_list)):
        for j in range(len(below_list[i])):
            below_list_filled[i][j] += below_list[i][j]
    above_list_rev = []
    for i in range(len(above_list_filled[0])):
        temp = []
        for j in range(len(above_list_filled)):
            temp.append(above_list_filled[j][i])
        above_list_rev.append(temp)
    equal_list_rev = []
    for i in range(len(equal_list_filled[0])):
        temp = []
        for j in range(len(equal_list_filled)):
            temp.append(equal_list_filled[j][i])
        equal_list_rev.append(temp)
    below_list_rev = []
    for i in range(len(below_list_filled[0])):
        temp = []
        for j in range(len(below_list_filled)):
            temp.append(below_list_filled[j][i])
        below_list_rev.append(temp)
    mean_above = []
    std_above = []
    mean_equal = []
    std_equal = []
    mean_below = []
    std_below = []
    for i in above_list_rev:
        mean_above.append(np.nanmean(i))
        std_above.append(np.nanstd(i))
    for i in equal_list_rev:
        mean_equal.append(np.nanmean(i))
        std_equal.append(np.nanstd(i))
    for i in below_list_rev:
        mean_below.append(np.nanmean(i))
        std_below.append(np.nanstd(i))

    mean_above_ = []
    mean_equal_ = []
    mean_below_ = []
    std_above_ = []
    std_equal_ = []
    std_below_ = []
    n_list_ = []
    temp_mean_above = 0
    temp_mean_equal = 0
    temp_mean_below = 0
    temp_std_above = 0
    temp_std_equal = 0
    temp_std_below = 0
    bar_size_count = 0
    for i in range(len(mean_above)):
        temp_mean_above += mean_above[i]
        temp_mean_equal += mean_equal[i]
        temp_mean_below += mean_below[i]
        temp_std_above += std_above[i]
        temp_std_equal += std_equal[i]
        temp_std_below += std_below[i]
        bar_size_count += 1
        if i+1 == len(mean_above):
            mean_above_.append(temp_mean_above)
            mean_equal_.append(temp_mean_equal)
            mean_below_.append(temp_mean_below)
            std_above_.append(temp_std_above)
            std_equal_.append(temp_std_equal)
            std_below_.append(temp_std_below)
            n_list_.append(n_list[i])
        elif bar_size_count >= BarSize:
            mean_above_.append(temp_mean_above)
            mean_equal_.append(temp_mean_equal)
            mean_below_.append(temp_mean_below)
            std_above_.append(temp_std_above)
            std_equal_.append(temp_std_equal)
            std_below_.append(temp_std_below)
            n_list_.append(n_list[i])
            temp_mean_above = 0
            temp_mean_equal = 0
            temp_mean_below = 0
            temp_std_above = 0
            temp_std_equal = 0
            temp_std_below = 0
            bar_size_count = 0
    mean_above_ = np.array(mean_above_)
    mean_equal_ = np.array(mean_equal_)
    mean_below_ = np.array(mean_below_)
    std_above_ = np.array(std_above_)
    std_equal_ = np.array(std_equal_)
    std_below_ = np.array(std_below_)
    n_list_ = np.array(n_list_)

    if DivideSize != 0:
        below_label = DivideSpecies + '<' + str(DivideSize)
        equal_label = DivideSpecies + '=' + str(DivideSize)
        above_label = DivideSpecies + '>' + str(DivideSize)
    else:
        above_label = 'With ' + DivideSpecies
        equal_label = 'Without ' + DivideSpecies
    if FileNum != 1:
        if DivideSize != 0:
            plt.bar(n_list_, mean_below_, width=BarSize, color='C0',
                    yerr=std_below_, label=below_label, ecolor='C3', capsize=2)
        plt.bar(n_list_, mean_equal_, width=BarSize, color='C1', yerr=std_equal_,
                bottom=mean_below_, label=equal_label, ecolor='C3', capsize=2)
        plt.bar(n_list_, mean_above_, width=BarSize, color='C2', yerr=std_above_,
                bottom=mean_below_+mean_equal_, label=above_label, ecolor='C3', capsize=2)
    else:
        if DivideSize != 0:
            plt.bar(n_list_, mean_below_, width=BarSize,
                    color='C0', label=below_label, capsize=2)
        plt.bar(n_list_, mean_equal_, width=BarSize, color='C1',
                bottom=mean_below_, label=equal_label, capsize=2)
        plt.bar(n_list_, mean_above_, width=BarSize, color='C2',
                bottom=mean_below_+mean_equal_, label=above_label, capsize=2)
    if xAxis == 'tot':
        x_label_name = 'total monomers'
    else:
        x_label_name = xAxis
    plt.xlabel('# of ' + x_label_name + ' in sigle complex')
    plt.ylabel('Count')
    plt.legend()
    plt.title('Histogram of Multi-component Assemblies')
    fig_name = 'stacked_histogram_of_' + xAxis + '_divided_by_' + DivideSpecies
    if SaveFig:
        plt.savefig(fig_name, dpi=500)
    plt.show()
    return n_list_, [mean_below_, mean_equal_, mean_above_], 'Nan', [std_below_, std_equal_, std_above_]


def multi_max_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesList: list, SpeciesName: str, SaveFig: bool = False):

    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    total_time_list.append(time)
                    temp_size_list = []
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if SpeciesName == 'tot':
                                total_size = sum(hist_list[j][k][0:-1])
                            elif SpeciesName in SpeciesList:
                                name_index = SpeciesList.index(SpeciesName)
                                total_size = hist_list[j][k][name_index]
                            else:
                                print('SpeciesName not in SpeciesList!')
                                return 0
                            temp_size_list.append(total_size)
                    total_size_list.append(max(temp_size_list))
        size_list.append(total_size_list)
        time_list.append(total_time_list)
    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in size_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    mean = np.array(mean)
    std = np.array(std)

    errorbar_color = '#c9e3f6'
    plt.plot(time_list[0], mean, color='C0')
    if FileNum > 1:
        plt.errorbar(time_list[0], mean, color='C0',
                     yerr=std, ecolor=errorbar_color)
    if SpeciesName == 'tot':
        title_spec = 'Total Species'
    else:
        title_spec = SpeciesName
    plt.title('Maximum Number of ' + str(title_spec) + ' in Single Complex')
    plt.xlabel('Time')
    plt.ylabel('Maximum Number of ' + str(title_spec))
    if SaveFig:
        plt.savefig('multi_max_complex.png', dpi=500)
    plt.show()
    return time_list[0], mean, 'Nan', std


def multi_mean_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesList: list, SpeciesName: str, ExcludeSize: int = 0, SaveFig: bool = False):

    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    total_time_list.append(time)
                    temp_sum = 0
                    count = 0
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if SpeciesName == 'tot':
                                total_size = sum(hist_list[j][k][0:-1])
                            elif SpeciesName in SpeciesList:
                                name_index = SpeciesList.index(SpeciesName)
                                total_size = hist_list[j][k][name_index]
                            else:
                                print('SpeciesName not in SpeciesList!')
                                return 0

                            if total_size >= ExcludeSize:
                                count += hist_list[j][k][-1]
                                temp_sum += total_size * hist_list[j][k][-1]
                    if count != 0:
                        total_size_list.append(temp_sum/count)
                    else:
                        total_size_list.append(0.0)
        size_list.append(total_size_list)
        time_list.append(total_time_list)
    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in size_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    mean = np.array(mean)
    std = np.array(std)

    errorbar_color = '#c9e3f6'
    plt.plot(time_list[0], mean, color='C0')
    if FileNum > 1:
        plt.errorbar(time_list[0], mean, color='C0',
                     yerr=std, ecolor=errorbar_color)
    if SpeciesName == 'tot':
        title_spec = 'Total Species'
    else:
        title_spec = SpeciesName
    plt.title('Maximum Number of ' + str(title_spec) + ' in Single Complex')
    plt.xlabel('Time')
    plt.ylabel('Maximum Number of ' + str(title_spec))
    if SaveFig:
        plt.savefig('multi_max_complex.png', dpi=500)
    plt.show()
    return time_list[0], mean, 'Nan', std


def multi_heatmap(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesList: list, xAxis: str, yAxis: str, xBarSize: int = 1, yBarSize: int = 1, ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    count_list_sum = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        x_size_list = []
        y_size_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis in SpeciesList and yAxis in SpeciesList:
                                x_name_index = SpeciesList.index(xAxis)
                                x_size = hist_list[j][k][x_name_index]
                                x_size = int(x_size / xBarSize)
                                y_name_index = SpeciesList.index(yAxis)
                                y_size = hist_list[j][k][y_name_index]
                                y_size = int(y_size / yBarSize)
                                if x_size not in x_size_list:
                                    if len(x_size_list) == 0:
                                        for m in range(0, x_size+1):
                                            x_size_list.append(m)
                                    else:
                                        if x_size - x_size_list[-1] == 1:
                                            x_size_list.append(x_size)
                                        else:
                                            diff = x_size - x_size_list[-1]
                                            for m in range(x_size_list[-1]+1, x_size+1):
                                                x_size_list.append(m)
                                if y_size not in y_size_list:
                                    if len(y_size_list) == 0:
                                        for m in range(0, y_size+1):
                                            y_size_list.append(m)
                                    else:
                                        if y_size - y_size_list[-1] == 1:
                                            y_size_list.append(y_size)
                                        else:
                                            for m in range(y_size_list[-1]+1, y_size+1):
                                                y_size_list.append(m)
                            else:
                                print('xAxis or yAxos not in SpeciesList!')
                                return 0
        count_list = np.zeros([len(y_size_list), len(x_size_list)])
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            count = hist_list[j][k][-1]
                            x_name_index = SpeciesList.index(xAxis)
                            x_size = hist_list[j][k][x_name_index]
                            x_size = int(x_size / xBarSize)
                            y_name_index = SpeciesList.index(yAxis)
                            y_size = hist_list[j][k][y_name_index]
                            y_size = int(y_size / yBarSize)
                            count_list[y_size][x_size] += count
        count_list = count_list/data_count
        count_list_sum.append(count_list)
    max_x = 0
    max_y = 0
    for i in count_list_sum:
        if len(i[0]) > max_x:
            max_x = len(i[0])
        if len(i) > max_y:
            max_y = len(i)
    count_list_sum_ = []
    for i in range(len(count_list_sum)):
        temp_matrix = np.zeros([max_y, max_x])
        for j in range(len(count_list_sum[i])):
            for k in range(len(count_list_sum[i][j])):
                temp_matrix[j][k] += count_list_sum[i][j][k]
        count_list_sum_.append(temp_matrix)
    count_list_mean = np.zeros([max_y, max_x])
    count_list_std = np.zeros([max_y, max_x])
    for i in range(len(count_list_sum_[0])):
        for j in range(len(count_list_sum_[0][0])):
            temp_list = []
            for k in range(len(count_list_sum_)):
                temp_list.append(count_list_sum_[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    x_list = np.arange(0, max_x) * xBarSize
    y_list = np.arange(0, max_y) * yBarSize

    fig, ax = plt.subplots()
    im = ax.imshow(count_list_mean)
    ax.set_xticks(np.arange(len(x_list)))
    ax.set_yticks(np.arange(len(y_list)))
    ax.set_xticklabels(x_list)
    ax.set_yticklabels(y_list)
    if ShowMean and ShowStd:
        print('Cannot show both maen and std!')
        return 0
    if ShowMean:
        fig_name = 'Complex_Distribution_of_' + xAxis + '_and_' + yAxis + '_with_mean'
        for i in range(len(y_list)):
            for j in range(len(x_list)):
                text = ax.text(j, i, round(
                    count_list_mean[i, j], 1), ha='center', va='center', color='w')
    elif ShowStd and FileNum != 1:
        fig_name = 'Complex_Distribution_of_' + xAxis + '_and_' + yAxis + '_with_std'
        for i in range(len(y_list)):
            for j in range(len(x_list)):
                text = ax.text(j, i, round(
                    count_list_std[i, j], 1), ha='center', va='center', color='w')
    else:
        fig_name = 'Complex_Distribution_of_' + xAxis + '_and_' + yAxis
    ax.set_title('Complex Distribution of ' + xAxis + ' and ' + yAxis)
    fig.tight_layout()
    plt.colorbar(im)
    plt.xlabel('Count of ' + xAxis)
    plt.ylabel('Count of ' + yAxis)
    if SaveFig:
        plt.savefig(fig_name, dpi=500,  bbox_inches='tight')
    plt.show()
    return x_list, y_list, count_list_mean, count_list_std


def multi_3D_hist(FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesList: list, xAxis: str, yAxis: str, xBarSize: int = 1, yBarSize: int = 1, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    count_list_sum = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        x_size_list = []
        y_size_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis in SpeciesList and yAxis in SpeciesList:
                                x_name_index = SpeciesList.index(xAxis)
                                true_x_size = hist_list[j][k][x_name_index]
                                x_size = int(true_x_size / xBarSize)
                                y_name_index = SpeciesList.index(yAxis)
                                true_y_size = hist_list[j][k][y_name_index]
                                y_size = int(true_y_size / yBarSize)
                                if x_size not in x_size_list:
                                    if len(x_size_list) == 0:
                                        for m in range(0, x_size+1):
                                            x_size_list.append(m)
                                    else:
                                        if x_size - x_size_list[-1] == 1:
                                            x_size_list.append(x_size)
                                        else:
                                            diff = x_size - x_size_list[-1]
                                            for m in range(x_size_list[-1]+1, x_size+1):
                                                x_size_list.append(m)
                                if y_size not in y_size_list:
                                    if len(y_size_list) == 0:
                                        for m in range(0, y_size+1):
                                            y_size_list.append(m)
                                    else:
                                        if y_size - y_size_list[-1] == 1:
                                            y_size_list.append(y_size)
                                        else:
                                            for m in range(y_size_list[-1]+1, y_size+1):
                                                y_size_list.append(m)
                            else:
                                print('xAxis or yAxos not in SpeciesList!')
                                return 0
        count_list = np.zeros([len(y_size_list), len(x_size_list)])
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            count = hist_list[j][k][-1]
                            x_name_index = SpeciesList.index(xAxis)
                            x_size = hist_list[j][k][x_name_index]
                            x_size = int(x_size / xBarSize)
                            y_name_index = SpeciesList.index(yAxis)
                            y_size = hist_list[j][k][y_name_index]
                            y_size = int(y_size / yBarSize)
                            count_list[y_size][x_size] += count
        count_list = count_list/data_count
        count_list_sum.append(count_list)
    max_x = 0
    max_y = 0
    for i in count_list_sum:
        if len(i[0]) > max_x:
            max_x = len(i[0])
        if len(i) > max_y:
            max_y = len(i)
    count_list_sum_ = []
    for i in range(len(count_list_sum)):
        temp_matrix = np.zeros([max_y, max_x])
        for j in range(len(count_list_sum[i])):
            for k in range(len(count_list_sum[i][j])):
                temp_matrix[j][k] += count_list_sum[i][j][k]
        count_list_sum_.append(temp_matrix)
    count_list_mean = np.zeros([max_y, max_x])
    count_list_std = np.zeros([max_y, max_x])
    for i in range(len(count_list_sum_[0])):
        for j in range(len(count_list_sum_[0][0])):
            temp_list = []
            for k in range(len(count_list_sum_)):
                temp_list.append(count_list_sum_[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    x_list = np.arange(0, max_x) * xBarSize
    y_list = np.arange(0, max_y) * yBarSize
    xx, yy = np.meshgrid(x_list, y_list)
    X, Y = xx.ravel(), yy.ravel()
    Z = count_list_mean.ravel()
    width = xBarSize
    depth = yBarSize
    bottom = np.zeros_like(Z)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.bar3d(X, Y, bottom, width, depth, Z, shade=True)
    ax.set_xlabel('# of ' + xAxis + ' in sigle complex')
    ax.set_ylabel('# of ' + yAxis + ' in sigle complex')
    ax.set_zlabel('Relative Occurrence Probability')
    ax.set_title('Complex Distribution of ' + xAxis + ' and ' + yAxis)
    fig.tight_layout()
    plt.xlabel('Count of ' + xAxis)
    plt.ylabel('Count of ' + yAxis)
    if SaveFig:
        plt.savefig('3D_hisogram_of_' + xAxis + '_and_' +
                    yAxis, dpi=500,  bbox_inches='tight')
    plt.show()
    return x_list, y_list, count_list_mean, 'Nan'


# --------------------------------Locate Position by Pdb or Restart----------------------------------


def PDB_pdb_to_df(file_name):
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name',
                      'Cite_Name', 'x_coord', 'y_coord', 'z_coord'])
    with open(file_name, 'r') as file:
        index = 0
        for line in file.readlines():
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                df.loc[index, 'Protein_Num'] = int(info[4])
                df.loc[index, 'Protein_Name'] = info[3]
                df.loc[index, 'Cite_Name'] = info[2]
                df.loc[index, 'x_coord'] = float(info[5])
                df.loc[index, 'y_coord'] = float(info[6])
                df.loc[index, 'z_coord'] = float(info[7])
            index += 1
        df = df.dropna()
        df = df.drop(index=df[(df.Cite_Name == 'COM')].index.tolist())
        df = df.reset_index(drop=True)
    return df


def PDB_dis_cal(x, y):
    return ((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)**0.5


def PDB_dis_df_gen(df, info):
    dis_df = pd.DataFrame(columns=['Protein_Num_1', 'Protein_Name_1', 'Cite_Name_1',
                          'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', 'dis'])
    index = 0
    count = 1
    for i in range(len(info)):
        df_temp_1 = df[df['Protein_Name'].isin([info.iloc[i, 0]])]
        df_1 = df_temp_1[df_temp_1['Cite_Name'].isin([info.iloc[i, 1]])]
        df_temp_2 = df[df['Protein_Name'].isin([info.iloc[i, 2]])]
        df_2 = df_temp_2[df_temp_2['Cite_Name'].isin([info.iloc[i, 3]])]
        df_1 = df_1.reset_index(drop=True)
        df_2 = df_2.reset_index(drop=True)
        print('Calculating distance for reaction #', count, '...')
        count += 1
        for j in range(len(df_1)):
            for k in range(len(df_2)):
                dis_df.loc[index, 'Protein_Num_1'] = df_1.loc[j, 'Protein_Num']
                dis_df.loc[index, 'Protein_Name_1'] = df_1.loc[j,
                                                               'Protein_Name']
                dis_df.loc[index, 'Cite_Name_1'] = df_1.loc[j, 'Cite_Name']
                dis_df.loc[index, 'Protein_Num_2'] = df_2.loc[k, 'Protein_Num']
                dis_df.loc[index, 'Protein_Name_2'] = df_2.loc[k,
                                                               'Protein_Name']
                dis_df.loc[index, 'Cite_Name_2'] = df_2.loc[k, 'Cite_Name']
                dis_df.loc[index, 'sigma'] = info.loc[i, 'sigma']
                x = [df_1.loc[j, 'x_coord'], df_1.loc[j,
                                                      'y_coord'], df_1.loc[j, 'z_coord']]
                y = [df_2.loc[k, 'x_coord'], df_2.loc[k,
                                                      'y_coord'], df_2.loc[k, 'z_coord']]
                dis_df.loc[index, 'dis'] = PDB_dis_cal(x, y)
                index += 1
    return dis_df


def PDB_bind_df_gen(dis_df, buffer_ratio):
    bind_df = pd.DataFrame(columns=['Protein_Num_1', 'Protein_Name_1', 'Cite_Name_1',
                           'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', 'dis'])
    index = 0
    for i in range(len(dis_df)):
        if dis_df.loc[i, 'dis'] >= dis_df.loc[i, 'sigma']*(1-buffer_ratio):
            if dis_df.loc[i, 'dis'] <= dis_df.loc[i, 'sigma']*(1+buffer_ratio):
                bind_df.loc[index] = dis_df.loc[i]
                index += 1
    return bind_df


def PDB_find_bond(bind_df):
    bond_lst = []
    for i in range(len(bind_df)):
        bond_lst.append([int(bind_df.loc[i, 'Protein_Num_1']),
                        int(bind_df.loc[i, 'Protein_Num_2'])])
    for i in bond_lst:
        i.sort()
    bond_lst_ = []
    for i in bond_lst:
        if i not in bond_lst_:
            bond_lst_.append(i)
    return bond_lst_


def PDB_find_complex(pdb_df, bond_lst):
    complex_lst = []
    for i in range(1, 1+pdb_df['Protein_Num'].max()):
        complex_temp = [i]
        j = 0
        while j < len(bond_lst):
            if bond_lst[j][0] in complex_temp and bond_lst[j][1] not in complex_temp:
                complex_temp.append(bond_lst[j][1])
                j = 0
            elif bond_lst[j][1] in complex_temp and bond_lst[j][0] not in complex_temp:
                complex_temp.append(bond_lst[j][0])
                j = 0
            else:
                j += 1
        complex_lst.append(complex_temp)
    for i in complex_lst:
        i.sort()
    complex_lst_ = []
    for i in complex_lst:
        if i not in complex_lst_:
            complex_lst_.append(i)
    return complex_lst_


def PDB_complex_df_gen(pdb_df, complex_lst):
    name_lst = list(pdb_df['Protein_Name'])
    name_lst_ = []
    for i in name_lst:
        if i not in name_lst_:
            name_lst_.append(i)
    column_lst = []
    for i in name_lst_:
        column_lst.append(i)
    column_lst.append('Protein_Num')
    complex_df = pd.DataFrame(columns=column_lst)
    index = 0
    for i in complex_lst:
        complex_df.loc[index] = 0
        complex_df.loc[index, 'Protein_Num'] = str(i)
        for j in i:
            for indexs in pdb_df.index:
                for k in range(len(pdb_df.loc[indexs].values)):
                    if(pdb_df.loc[indexs].values[k] == j):
                        col = pdb_df.loc[indexs, 'Protein_Name']
                        complex_df.loc[index, col] += 1
                        break
                else:
                    continue
                break
        index += 1
    return complex_df


def PDB_find_complex_df(complex_df, num_lst, pdb_df):
    protein_name = []
    for i in range(len(pdb_df)):
        if pdb_df.loc[i, 'Protein_Name'] not in protein_name:
            protein_name.append(pdb_df.loc[i, 'Protein_Name'])
    complex_df['Num_List'] = ''
    for i in range(complex_df.shape[0]):
        lst = []
        for j in range(complex_df.shape[1]-2):
            lst.append(complex_df.iloc[i, j])
        complex_df.loc[i, 'Num_List'] = str(lst)
    num_lst_str = str(num_lst)
    protein_remain = []
    for i in range(complex_df.shape[0]):
        if complex_df.loc[i, 'Num_List'] == num_lst_str:
            string = complex_df.loc[i, 'Protein_Num']
            string = string.strip('[').strip(']').split(',')
            for i in string:
                protein_remain.append(int(i))
    return protein_remain


def PDB_new_pdb(file_name, protein_remain):
    with open(file_name, 'r') as file:
        write_lst = []
        for line in file.readlines():
            line_ = line.split(' ')
            if line_[0] == 'TITLE':
                write_lst.append(line)
            elif line_[0] == 'CRYST1':
                write_lst.append(line)
            elif line_[0] == 'ATOM':
                info = []
                for i in line_:
                    i.strip('\n')
                    if i != '':
                        info.append(i)
                info[9] = info[9].strip('\n')
                if int(info[4]) in protein_remain:
                    write_lst.append(line)
    with open('output_file.pdb', 'w') as file_:
        file_.seek(0)
        file_.truncate()
        for i in write_lst:
            file_.writelines(i)
    return 0


def PDB_binding_info_df(inp_name):
    status = False
    index = -1
    binding_info = pd.DataFrame(
        columns=['Protein_Name_1', 'Cite_Name_1', 'Protein_Name_2', 'Cite_Name_2', 'sigma'])
    with open(inp_name, 'r') as file:
        for line in file.readlines():
            if line == 'end reactions\n':
                status = False
                break
            if line == 'start reactions\n':
                status = True
            if status:
                if '<->' in line:
                    index += 1
                    line1 = line.split('+')
                    element1 = line1[0].strip(' ')
                    line2 = line1[1].split('<->')
                    element2 = line2[0].strip(' ')
                    element1_ = element1.strip(')').split('(')
                    element2_ = element2.strip(')').split('(')
                    binding_info.loc[index,
                                     'Protein_Name_1'] = element1_[0][0:3]
                    binding_info.loc[index, 'Cite_Name_1'] = element1_[1][0:3]
                    binding_info.loc[index,
                                     'Protein_Name_2'] = element2_[0][0:3]
                    binding_info.loc[index, 'Cite_Name_2'] = element2_[1][0:3]
                if 'sigma' in line:
                    binding_info.loc[index, 'sigma'] = float(
                        line.split(' = ')[-1].strip('\n'))
    return binding_info


def locate_position_PDB(FileNamePdb, NumList, FileNameInp, BufferRatio=0.01):
    print('Reading files......')
    pdb_df = PDB_pdb_to_df(FileNamePdb)
    print('Reading files complete!')
    print('Extracting binding information......')
    binding_info = PDB_binding_info_df(FileNameInp)
    print('Extracting complete!')
    print('Calculating distance......')
    dis_df = PDB_dis_df_gen(pdb_df, binding_info)
    print('Calculation complete!')
    print('Finding bonds......')
    bind_df = PDB_bind_df_gen(dis_df, BufferRatio)
    bond_lst = PDB_find_bond(bind_df)
    print('Finding bonds complete!')
    print('Finding complexes......')
    complex_lst = PDB_find_complex(pdb_df, bond_lst)
    complex_df = PDB_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')
    print('Writing new PDB files......')
    protein_remain = PDB_find_complex_df(complex_df, NumList, pdb_df)
    PDB_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


def RESTART_read_restart(file_name_restart):
    with open(file_name_restart, 'r') as file:
        status = False
        count = 0
        complex_lst = []
        for line in file.readlines():
            if line == '#All Complexes and their components \n':
                status = True
            if status:
                if count % 8 == 7:
                    info = line.split()
                    temp_lst = []
                    for i in range(len(info)):
                        if i != 0:
                            temp_lst.append(int(info[i]))
                    complex_lst.append(temp_lst)
                count += 1
            if line == '#Observables \n':
                break
    print('The total number of complexes is', len(complex_lst))
    return complex_lst


def RESTART_pdb_to_df(file_name_pdb):
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name'])
    with open(file_name_pdb, 'r') as file:
        index = 0
        for line in file.readlines():
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                df.loc[index, 'Protein_Num'] = int(info[4])
                df.loc[index, 'Protein_Name'] = info[3]
            index += 1
        df = df.dropna()
        df = df.reset_index(drop=True)
    return df


def RESTART_complex_df_gen(pdb_df, complex_lst):
    name_lst = list(pdb_df['Protein_Name'])
    name_lst_ = []
    for i in name_lst:
        if i not in name_lst_:
            name_lst_.append(i)
    column_lst = []
    for i in name_lst_:
        column_lst.append(i)
    column_lst.append('Protein_Num')
    complex_df = pd.DataFrame(columns=column_lst)
    index = 0
    for i in complex_lst:
        complex_df.loc[index] = 0
        complex_df.loc[index, 'Protein_Num'] = str(i)
        for j in i:
            for indexs in pdb_df.index:
                for k in range(len(pdb_df.loc[indexs].values)):
                    if(pdb_df.loc[indexs].values[k] == j):
                        col = pdb_df.loc[indexs, 'Protein_Name']
                        complex_df.loc[index, col] += 1
                        break
                else:
                    continue
                break
        index += 1
    return complex_df


def RESTART_find_complex_df(complex_df, num_lst, pdb_df):
    protein_name = []
    for i in range(len(pdb_df)):
        if pdb_df.loc[i, 'Protein_Name'] not in protein_name:
            protein_name.append(pdb_df.loc[i, 'Protein_Name'])
    complex_df['Num_List'] = ''
    for i in range(complex_df.shape[0]):
        lst = []
        for j in range(complex_df.shape[1]-2):
            lst.append(complex_df.iloc[i, j])
        complex_df.loc[i, 'Num_List'] = str(lst)
    num_lst_str = str(num_lst)
    protein_remain = []
    for i in range(complex_df.shape[0]):
        if complex_df.loc[i, 'Num_List'] == num_lst_str:
            string = complex_df.loc[i, 'Protein_Num']
            string = string.strip('[').strip(']').split(',')
            for i in string:
                protein_remain.append(int(i))
    return protein_remain


def RESTART_new_pdb(file_name_pdb, protein_remain):
    with open(file_name_pdb, 'r') as file:
        write_lst = []
        for line in file.readlines():
            line_ = line.split(' ')
            if line_[0] == 'TITLE':
                write_lst.append(line)
            elif line_[0] == 'CRYST1':
                write_lst.append(line)
            elif line_[0] == 'ATOM':
                info = []
                for i in line_:
                    i.strip('\n')
                    if i != '':
                        info.append(i)
                info[9] = info[9].strip('\n')
                if int(info[4]) in protein_remain:
                    write_lst.append(line)
    with open('output_file.pdb', 'w') as file_:
        file_.seek(0)
        file_.truncate()
        for i in write_lst:
            file_.writelines(i)
    return 0


def locate_position_restart(FileNamePdb, NumList, FileNameRestart='restart.dat'):
    print('Reading restart.dat......')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')
    print('Reading PDB files......')
    pdb_df = RESTART_pdb_to_df(FileNamePdb)
    print('Reading files complete!')
    print('Finding complexes......')
    complex_df = RESTART_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')
    print('Writing new PDB files......')
    protein_remain = RESTART_find_complex_df(complex_df, NumList, pdb_df)
    RESTART_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


def single_locate_position_restart(FileNamePdb, ComplexSize, FileNameRestart = 'restart.dat'):
    print('Reading restart.dat...')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')
    protein_remain = []
    for i in complex_lst:
        if len(i) == ComplexSize:
            protein_remain.append(i)
    protein_remain_flat = []
    for i in protein_remain:
        for j in i:
            protein_remain_flat.append(j)
    RESTART_new_pdb(FileNamePdb, protein_remain_flat)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0



# ---------------------------Reading Real PDB File and Generating NERDSS inputs-----------------------------------
# function for checking format of data in readlines
def real_PDB_data_check(data):
    if len(data) != 12:
        if len(data[2]) > 4:
            return -1  # Amino acid name stick with info before
    else:
        if len(data[3]) == 3:
            return 1  # True data
        else:
            return -2  # Wrong amino acid name


# This function will go over every atom between two chains to determine whether they are interacting (distance smaller
# than 3.0A)
# remember to import math package when use the function
# Input variables:
# return variables: a tuple includes
def real_PDB_chain_int(unique_chain, split_position, split_resi_count, split_atom_count, split_resi_type, split_atom_type, split_resi_position):
    distance = 0
    # list of lists (each sublist will include two letters indicating these two chains have
    reaction_chain = []
    # interaction) eg: in this protein, only chain A&B, A&D and C&D are interacting, then the list will look like
    # [[A,B],[A,D],[C,D]]
    # list of lists of lists(each sub-sublist will include a bunch of lists of residue pairs
    reaction_resi_type = []
    # (without repeats)) eg: [[[resia,resib],[resic,resid]],[[resie,resif],[resig,resih]],[[resii,resij],[resik,resil]]]
    # ----reaction residues of chain-------- A&B------------------------A&D-------------------------C&D -------------
    reaction_resi_count = []
    reaction_atom = []
    reaction_atom_position = []
    reaction_atom_distance = []
    reaction_atom_type = []
    reaction_resi_position = []
    for i in range(len(unique_chain) - 1):
        for j in range(i+1, len(unique_chain)):
            inner_atom_position = []
            inner_atom_distance = []
            inner_atom = []
            inner_reaction_resi_count = []
            inner_reaction_resi_type = []
            inner_reaction_atom_type = []
            inner_reaction_resi_position = []
            for m in range(len(split_position[i])):
                for n in range(len(split_position[j])):
                    distance = math.sqrt((split_position[i][m][0]-split_position[j][n][0])**2
                                         + (split_position[i][m][1]-split_position[j][n][1])**2
                                         + (split_position[i][m][2]-split_position[j][n][2])**2)
                    if distance <= 0.3:
                        inner_atom.append(
                            [split_atom_count[i][m], split_atom_count[j][n]])
                        inner_atom_distance.append(distance)
                        inner_atom_position.append(
                            [split_position[i][m], split_position[j][n]])
                        inner_reaction_atom_type.append(
                            [split_atom_type[i][m], split_atom_type[j][n]])
                        if [split_resi_count[i][m], split_resi_count[j][n]] not in inner_reaction_resi_count:
                            inner_reaction_resi_count.append(
                                [split_resi_count[i][m], split_resi_count[j][n]])
                            inner_reaction_resi_position.append(
                                [split_resi_position[i][m], split_resi_position[j][n]])
                            inner_reaction_resi_type.append(
                                [split_resi_type[i][m], split_resi_type[j][n]])
            if len(inner_reaction_resi_count) > 0:
                reaction_chain.append([unique_chain[i], unique_chain[j]])
                reaction_resi_count.append(inner_reaction_resi_count)
                reaction_resi_type.append(inner_reaction_resi_type)
                reaction_atom.append(inner_atom)
                reaction_atom_position.append(inner_atom_position)
                reaction_atom_distance.append(inner_atom_distance)
                reaction_atom_type.append(inner_reaction_atom_type)
                reaction_resi_position.append(inner_reaction_resi_position)
    return reaction_chain, reaction_atom, reaction_atom_position, reaction_atom_distance, reaction_resi_count, \
        reaction_resi_type, reaction_atom_type, reaction_resi_position


def real_PDB_unit(x: np.ndarray) -> np.ndarray:
    '''Get the unit vector of x\n
    Return 0 if ||x||=0\n
    Return itself if ||x||=1'''
    x_norm = np.linalg.norm(x)
    if abs(x_norm-1) < 10**-6:
        return x
    elif x_norm < 10**-6:
        return np.zeros(3)
    else:
        return x/x_norm


def real_PDB_triangle_correction(x: float) -> float:
    '''make x in range of [-1, 1], correct precision'''
    if x < -1 and abs(x+1) < 10**-6:
        return -1
    elif x > 1 and abs(x-1) < 10**-6:
        return 1
    elif -1 <= x <= 1:
        return x
    else:
        raise ValueError(f'{x} is out of the range of sin/cos')


def real_PDB_calculate_phi(v: np.ndarray, n: np.ndarray, sigma: np.ndarray) -> float:

    # calculate phi
    t1 = real_PDB_unit(np.cross(v, sigma))
    t2 = real_PDB_unit(np.cross(v, n))
    phi = math.acos(real_PDB_triangle_correction(np.dot(t1, t2)))

    # determine the sign of phi (+/-)
    v_uni = real_PDB_unit(v)
    n_proj = n - v_uni * np.dot(v_uni, n)
    sigma_proj = sigma - v_uni * np.dot(v_uni, sigma)
    phi_dir = real_PDB_unit(np.cross(sigma_proj, n_proj))

    if np.dot(v_uni, phi_dir) > 0:
        phi = -phi
    else:
        phi = phi

    return phi


# This function will calculate five necessary angles: theta_one, theta_two, phi_one, phi_two and omega
# Input variables: four coordinates indicating COM and interaction site of two chains
# First created by Yian Qian
# Modified by Mankun Sang on 04/13/2022
#   1) unit of zero vector and length-one vector
#   2) error messages when v // n
#   3) test scripts
# Modified by Yian Qian & Mankun Sang on 04/16/2022
#   0) correct omega calculation when n // sigma
#   1) generalize the sign determination of phi and omega
#   2) created a function for phi cacluation
def real_PDB_angles(COM1, COM2, int_site1, int_site2, normal_point1, normal_point2):
    '''Calculate the angles for binding'''

    # Convert sequences into arrays for convinience
    COM1 = np.array(COM1)
    COM2 = np.array(COM2)
    int_site1 = np.array(int_site1)
    int_site2 = np.array(int_site2)
    normal_point1 = np.array(normal_point1)
    normal_point2 = np.array(normal_point2)

    # Get Vectors
    v1 = int_site1 - COM1  # from COM to interface (particle 1)
    v2 = int_site2 - COM2  # from COM to interface (particle 2)
    sigma1 = int_site1 - int_site2  # sigma, from p2 to p1
    sigma2 = int_site2 - int_site1  # sigma, from p1 to p2
    n1 = real_PDB_unit(normal_point1 - COM1)  # normal vector for p1
    n2 = real_PDB_unit(normal_point2 - COM2)  # normal vector for p2

    # Calculate the magnititude of sigma
    sigma_magnitude = np.linalg.norm(sigma1)

    # Calculate theta1 and theta2
    costheta1 = np.dot(v1, sigma1) / np.linalg.norm(v1) / \
        np.linalg.norm(sigma1)
    costheta2 = np.dot(v2, sigma2) / np.linalg.norm(v2) / \
        np.linalg.norm(sigma2)
    theta1 = math.acos(real_PDB_triangle_correction(costheta1))
    theta2 = math.acos(real_PDB_triangle_correction(costheta2))

    # check geometry
    errormsg = ''
    iferror = False  # determine if v // n
    if np.linalg.norm(np.cross(n1, v1)) < 10**-6:
        iferror = True
        errormsg += '\n\tn1 and v1 parallel, phi1 not available'
    if np.linalg.norm(np.cross(n2, v2)) < 10**-6:
        iferror = True
        errormsg += '\n\tn2 and v2 parallel, phi2 not available'
    if iferror:
        raise ValueError(errormsg)

    # determine if phi1 exists (v1 // sigma1 ?)
    if np.linalg.norm(np.cross(sigma1, v1)) < 10**-6:
        phi1 = float('nan')
        # omega_parallel = True
        omega_t1 = real_PDB_unit(np.cross(sigma1, n1))
    else:
        phi1 = real_PDB_calculate_phi(v1, n1, sigma1)
        omega_t1 = real_PDB_unit(np.cross(sigma1, v1))

    # determine if phi2 exists (v2 // sigma2 ?)
    if np.linalg.norm(np.cross(sigma2, v2)) < 10**-6:
        phi2 = float('nan')
        # omega_parallel = True
        omega_t2 = real_PDB_unit(np.cross(sigma1, n2))
    else:
        phi2 = real_PDB_calculate_phi(v2, n2, sigma2)
        omega_t2 = real_PDB_unit(np.cross(sigma1, v2))

    # calculate omega (both cases are same)
    omega = math.acos(real_PDB_triangle_correction(np.dot(omega_t1, omega_t2)))
    # determine the sign of omega (+/-)
    sigma1_uni = real_PDB_unit(sigma1)
    sigma1xomega_t1 = np.cross(sigma1, omega_t1)
    sigma1xomega_t2 = np.cross(sigma1, omega_t2)
    omega_dir = real_PDB_unit(np.cross(sigma1xomega_t1, sigma1xomega_t2))
    if np.dot(sigma1_uni, omega_dir) > 0:
        omega = -omega
    else:
        omega = omega

    return theta1, theta2, phi1, phi2, omega, sigma_magnitude


def real_PDB_norm_check(norm, COM, site, buffer_ratio=1e-3):
    '''
    norm is a 3D vector
    COM is a point
    site is a point
    False: continue norm calculation
    True: requesting redo input
    '''
    for i in norm:
        if type(i) != float:
            return True
    for i in COM:
        if type(i) != float:
            return True
    for i in site:
        if type(i) != float:
            return True
    if len(norm) != 3 or len(COM) != 3 or len(site) != 3:
        return True
    if norm == [0, 0, 0]:
        return True
    norm = np.array(norm)
    COM = np.array(COM)
    site = np.array(site)
    vec1 = norm
    vec2 = site - COM
    zero_pos_1 = []
    zero_pos_2 = []
    for i in range(len(vec1)):
        if vec1[i] == 0:
            zero_pos_1.append(i)
    for i in range(len(vec2)):
        if vec2[i] == 0:
            zero_pos_2.append(i)
    if len(zero_pos_1) == 1 and len(zero_pos_2) == 1 and zero_pos_1 == zero_pos_2:
        pool = [0, 1, 2]
        pool.remove(zero_pos_1[0])
        ratio = vec1[pool[0]]/vec2[pool[0]]
        if vec1[pool[1]]/vec2[pool[1]] >= ratio*(1-buffer_ratio) and vec1[pool[1]]/vec2[pool[1]] <= ratio*(1+buffer_ratio):
            return True
        else:
            return False
    elif len(zero_pos_1) == 1 and len(zero_pos_2) == 1 and zero_pos_1 != zero_pos_2:
        return False
    elif len(zero_pos_1) == 2 and len(zero_pos_2) == 2 and zero_pos_1 == zero_pos_2:
        return True
    elif len(zero_pos_1) == 2 and len(zero_pos_2) == 2 and zero_pos_1 != zero_pos_2:
        return False
    elif len(zero_pos_1) != len(zero_pos_2):
        return False
    else:
        ratio = vec1[0]/vec2[0]
        if ratio >= 0:
            if vec1[1]/vec2[1] >= ratio*(1-buffer_ratio) and vec1[1]/vec2[1] <= ratio*(1+buffer_ratio):
                if vec1[2]/vec2[2] >= ratio*(1-buffer_ratio) and vec1[2]/vec2[2] <= ratio*(1+buffer_ratio):
                    return True
                else:
                    return False
            else:
                return False
        if ratio < 0:
            if vec1[1]/vec2[1] >= ratio*(1+buffer_ratio) and vec1[1]/vec2[1] <= ratio*(1-buffer_ratio):
                if vec1[2]/vec2[2] >= ratio*(1+buffer_ratio) and vec1[2]/vec2[2] <= ratio*(1-buffer_ratio):
                    return True
                else:
                    return False
            else:
                return False


def real_PDB_norm_input(normal_point_lst, chain_name, chain_pair1, chain_pair2):
    normal_point_1_temp = input('Please input normal vector for ' +
                                chain_name + ' in chain ' + chain_pair1 + " & " + chain_pair2 + ' : ')
    normal_point_1_temp = normal_point_1_temp.strip('[').strip(']').split(',')
    normal_point_1_temp_ = []
    for j in normal_point_1_temp:
        normal_point_1_temp_.append(float(j))
    normal_point_lst.append(normal_point_1_temp_)
    return normal_point_lst


def real_PDB_mag(x):
    return math.sqrt(sum(i ** 2 for i in x))


def real_PDB_UI():
    # naming explanation:
    # variables with word 'total' in the front indicate that it's a list of data for the whole protein
    # variables with word 'split' in the front indicate that it's a list containing n sub-lists and each sub-list contains
    # data for different chains. (n is the number of chains)

    # indicating number of atoms: if there are 5 atoms, then the list looks like [1,2,3,4,5]
    total_atom_count = []
    # specific chain the atom belongs to (such as A or B or C, etc).
    total_chain = []
    total_resi_count = []  # residue number
    total_position = []  # the coordinate of each atom
    total_atom_type = []  # to show whether the atom is a alpha carbon, N, etc.
    total_resi_type = []  # to show the type of residue
    # indicate the position of alpha carbon of the residue the atom is in.
    total_resi_position_every_atom = []
    total_resi_position = []  # list of position of all alpha carbon atom position
    total_alphaC_resi_count = []  # indicate which residue the alphaC belongs to
    # The length of last two lists are the same as total residue numbers in the chain and the length of rest of the lists
    # are the same as total atom numbers in the protein.
    # read in user pdb file
    # out data into corresponding lists
    with open(input("Enter pdb file name: "), "r") as filename:
        for line in filename:
            data = line.split()  # split a line into list
            id = data[0]
            if id == 'ENDMDL':
                break
            if id == 'ATOM':  # find all 'atom' lines
                if real_PDB_data_check(data) == 1:
                    pass
                elif real_PDB_data_check(data) == -2:
                    data[3] = data[3].lstrip(data[3][0])
                elif real_PDB_data_check(data) == -1:
                    amino_name = data[2][-3:]
                    data.insert(3, amino_name)
                    data[2] = data[2].rstrip(amino_name)

                total_atom_count.append(data[1])
                total_chain.append(data[4])
                total_resi_count.append(data[5])
                total_atom_type.append(data[2])
                total_resi_type.append(data[3])
                # change all strings into floats for position values, also converting to nm from angstroms
                position_coords = []
                for i in range(3):
                    position_coords.append(float(data[6+i])/10)
                total_position.append(position_coords)
                if data[2] == "CA":
                    total_resi_position.append(position_coords)
                    total_alphaC_resi_count.append(data[5])
    print('Finish reading pdb file')

    # create total_resi_position_every_atom list
    count = 0
    for i in range(len(total_alphaC_resi_count)):
        if count >= len(total_atom_type):
            break
        for j in range(count, len(total_atom_type)):
            if total_resi_count[j] == total_alphaC_resi_count[i]:
                total_resi_position_every_atom.append(total_resi_position[i])
                count = count + 1
            else:
                break

    # determine how many unique chains exist
    unique_chain = []
    for letter in total_chain:
        if letter not in unique_chain:
            unique_chain.append(letter)
    print(str(len(unique_chain)) + ' chain(s) in total: ' + str(unique_chain))

    # exit if there's only one chain.
    if len(unique_chain) == 1:
        sys.exit()

    # create lists of lists where each sublist contains the data for different chains.
    split_atom_count = []
    split_chain = []
    split_resi_count = []
    split_position = []
    split_atom_type = []
    split_resi_type = []
    chain_end_atom = []
    split_resi_position_every_atom = []

    # inner lists are sublists of each list, each of the sublist represents data about a list
    inner_atom_count = []
    inner_chain = []
    inner_resi_count = []
    inner_position = []
    inner_atom_type = []
    inner_resi_type = []
    inner_resi_position_every_atom = []

    # determine number of atoms in each chain
    chain_counter = 0

    for i in range(len(total_atom_count)):

        if total_chain[i] != unique_chain[chain_counter]:
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(
                inner_resi_position_every_atom)
            inner_atom_count = []
            inner_chain = []
            inner_resi_count = []
            inner_position = []
            inner_atom_type = []
            inner_resi_type = []
            inner_resi_position_every_atom = []
            chain_end_atom.append(len(split_atom_count[chain_counter]))
            chain_counter = chain_counter + 1

        if total_chain[i] == unique_chain[chain_counter]:
            inner_atom_count.append(total_atom_count[i])
            inner_chain.append(total_chain[i])
            inner_resi_count.append(total_resi_count[i])
            inner_position.append(total_position[i])
            inner_atom_type.append(total_atom_type[i])
            inner_resi_type.append(total_resi_type[i])
            inner_resi_position_every_atom.append(
                total_resi_position_every_atom[i])

        if i == (len(total_atom_count) - 1):
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(
                inner_resi_position_every_atom)
            chain_end_atom.append(len(split_atom_count[chain_counter]))

    print('Each of them has ' + str(chain_end_atom) + ' atoms.')

    # determine the interaction between each two chains by using function chain_int()
    # the output is a tuple with 7 list of list including: reaction_chain, reaction_atom, reaction_atom_position,
    # reaction_atom_distance, reaction_resi_count, reaction_resi_type and  reaction_atom_type

    interaction = real_PDB_chain_int(unique_chain, split_position, split_resi_count, split_atom_count,
                                     split_resi_type, split_atom_type, split_resi_position_every_atom)
    reaction_chain = interaction[0]
    reaction_atom = interaction[1]
    reaction_atom_position = interaction[2]
    reaction_atom_distance = interaction[3]
    reaction_resi_count = interaction[4]
    reaction_resi_type = interaction[5]
    reaction_atom_type = interaction[6]
    reaction_resi_position = interaction[7]

    # calculating center of mass (COM) and interaction site

    # COM
    COM = []
    for i in range(len(split_position)):
        sumx = 0
        sumy = 0
        sumz = 0
        for j in range(len(split_position[i])):
            sumx = sumx + split_position[i][j][0]
            sumy = sumy + split_position[i][j][1]
            sumz = sumz + split_position[i][j][2]
        inner_COM = [sumx / len(split_position[i]), sumy /
                     len(split_position[i]), sumz / len(split_position[i])]
        COM.append(inner_COM)

    for i in range(len(COM)):
        print("Center of mass of  " + unique_chain[i] + " is: " +
              "[%.3f, %.3f, %.3f]" % (COM[i][0], COM[i][1], COM[i][2]))

    # int_site
    int_site = []
    two_chain_int_site = []

    for i in range(len(reaction_resi_position)):
        for j in range(0, 2):
            sumx = 0
            sumy = 0
            sumz = 0
            count = 0
            added_position = []
            for k in range(len(reaction_resi_position[i])):
                if reaction_resi_position[i][k][j] not in added_position:
                    sumx = sumx + reaction_resi_position[i][k][j][0]
                    sumy = sumy + reaction_resi_position[i][k][j][1]
                    sumz = sumz + reaction_resi_position[i][k][j][2]
                    added_position.append(reaction_resi_position[i][k][j])
                    count = count + 1
            inner_int_site = [sumx / count, sumy / count, sumz / count]
            two_chain_int_site.append(inner_int_site)
        int_site.append(two_chain_int_site)
        two_chain_int_site = []

    # calculate distance between interaction site.
    int_site_distance = []
    for i in range(len(int_site)):
        distance = math.sqrt((int_site[i][0][0] - int_site[i][1][0]) ** 2 + (int_site[i][0][1] - int_site[i][1][1]) ** 2
                             + (int_site[i][0][2] - int_site[i][1][2]) ** 2)
        int_site_distance.append(distance)

    for i in range(len(int_site)):
        print("Interaction site of " + reaction_chain[i][0] + " & " + reaction_chain[i][1] + " is: "
              + "[%.3f, %.3f, %.3f]" % (int_site[i][0][0],
                                        int_site[i][0][1], int_site[i][0][2]) + " and "
              + "[%.3f, %.3f, %.3f]" % (int_site[i][1][0],
                                        int_site[i][1][1], int_site[i][1][2])
              + " distance between interaction sites is: %.3f nm" % (int_site_distance[i]))

    # user can choose to change the interaction site
    new_int_site_distance = copy.deepcopy(int_site_distance)
    new_int_site = copy.deepcopy(int_site)

    while True:
        answer = input(
            "Would you like to change the distance between interaction site (Type 'yes' or 'no'): ")
        if answer == "no":
            print("Calculation is completed.")
            break
        if answer == "yes":
            while True:
                n = int(input("Which distance would you like to change (please enter an integer no greater than %.0f or enter 0 to set all distance to a specific number): " % (
                    len(int_site_distance)))) - 1
                if n in range(-1, len(int_site_distance)):
                    while True:
                        new_distance = float(
                            input("Please enter new distance: "))
                        # decreasing distance & increasing distance
                        if new_distance >= 0:
                            if n == -1:
                                for p in range(0, len(reaction_chain)):
                                    new_int_site_distance[p] = copy.deepcopy(
                                        new_distance)
                                    dir_vec1 = (
                                        int_site[p][0][0] -
                                        int_site[p][1][0], int_site[p][0][1] -
                                        int_site[p][1][1],
                                        int_site[p][0][2] - int_site[p][1][2])
                                    dir_vec2 = (
                                        int_site[p][1][0] -
                                        int_site[p][0][0], int_site[p][1][1] -
                                        int_site[p][0][1],
                                        int_site[p][1][2] - int_site[p][0][2])
                                    unit_dir_vec1 = [dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1),
                                                     dir_vec1[2] / real_PDB_mag(dir_vec1)]
                                    unit_dir_vec2 = [dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2),
                                                     dir_vec2[2] / real_PDB_mag(dir_vec2)]

                                    inner_new_position = []
                                    new_coord1 = []
                                    new_coord2 = []
                                    for i in range(3):
                                        new_coord1.append(
                                            (new_distance - int_site_distance[p]) / 2 * unit_dir_vec1[i] + int_site[p][0][
                                                i])
                                        new_coord2.append(
                                            (new_distance - int_site_distance[p]) / 2 * unit_dir_vec2[i] + int_site[p][1][
                                                i])
                                    inner_new_position.append(new_coord1)
                                    inner_new_position.append(new_coord2)

                                    new_int_site[p] = copy.deepcopy(
                                        inner_new_position)
                                    new_int_site_distance[p] = math.sqrt(
                                        (new_int_site[p][0][0] -
                                         new_int_site[p][1][0]) ** 2
                                        + (new_int_site[p][0][1] -
                                           new_int_site[p][1][1]) ** 2
                                        + (new_int_site[p][0][2] - new_int_site[p][1][2]) ** 2)
                                    print("New interaction site of " + reaction_chain[p][0] + " & " + reaction_chain[p][
                                        1] + " is: "
                                        + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[p][0][0], new_int_site[p][0][1], new_int_site[p][0][2]) + " and "
                                        + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[p][1][0], new_int_site[p][1][1], new_int_site[p][1][2])
                                        + " distance between interaction sites is: %.3f" % (new_int_site_distance[p]))
                                break
                            if n >= 0:
                                new_int_site_distance[n] = copy.deepcopy(
                                    new_distance)
                                dir_vec1 = (int_site[n][0][0] - int_site[n][1][0], int_site[n][0]
                                            [1] - int_site[n][1][1], int_site[n][0][2] - int_site[n][1][2])
                                dir_vec2 = (int_site[n][1][0] - int_site[n][0][0], int_site[n][1]
                                            [1] - int_site[n][0][1], int_site[n][1][2] - int_site[n][0][2])
                                unit_dir_vec1 = [
                                    dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1), dir_vec1[2] / real_PDB_mag(dir_vec1)]
                                unit_dir_vec2 = [
                                    dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2), dir_vec2[2] / real_PDB_mag(dir_vec2)]

                                inner_new_position = []
                                new_coord1 = []
                                new_coord2 = []
                                for i in range(3):
                                    new_coord1.append(
                                        (new_distance - int_site_distance[n]) / 2 * unit_dir_vec1[i] + int_site[n][0][i])
                                    new_coord2.append(
                                        (new_distance - int_site_distance[n]) / 2 * unit_dir_vec2[i] + int_site[n][1][i])
                                inner_new_position.append(new_coord1)
                                inner_new_position.append(new_coord2)

                                new_int_site[n] = copy.deepcopy(
                                    inner_new_position)
                                new_int_site_distance[n] = math.sqrt((new_int_site[n][0][0] - new_int_site[n][1][0]) ** 2
                                                                     + (new_int_site[n][0][1] - new_int_site[n][1][1]) ** 2
                                                                     + (new_int_site[n][0][2] - new_int_site[n][1][2]) ** 2)
                                print("New interaction site of " + reaction_chain[n][0] + " & " + reaction_chain[n][1] + " is: "
                                      + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[n][0][0], new_int_site[n][0][1], new_int_site[n][0][2]) + " and "
                                      + "[%.3f, %.3f, %.3f]" % (
                                    new_int_site[n][1][0], new_int_site[n][1][1], new_int_site[n][1][2])
                                    + " distance between interaction sites is: %.3f" % (new_int_site_distance[n]))
                                break
                        else:
                            print('Invalid number, please try again.')
                            break
                    break
                else:
                    print("Invalid answer, please try again.")
                    break
        else:
            print("Invalid answer, please try again.")

    # ditermine sigma
    # calculating angles
    angle = []
    normal_point_lst1 = []
    normal_point_lst2 = []

    while True:
        answer_norm = str(
            input("Would you like to use the default norm vector (0,0,1)? (Type 'yes' or 'no'): "))
        if answer_norm == 'yes' or answer_norm == 'no':
            break

    # type in norm
    if answer_norm == 'no':
        for i in range(len(reaction_chain)):
            chain1 = 0
            chain2 = 0
            for j in range(len(unique_chain)):
                if reaction_chain[i][0] == unique_chain[j]:
                    chain1 = j
                if reaction_chain[i][1] == unique_chain[j]:
                    chain2 = j
                if reaction_chain[i][0] == unique_chain[chain1] and reaction_chain[i][1] == unique_chain[chain2]:
                    break
            while True:
                normal_point_lst1 = real_PDB_norm_input(normal_point_lst1, str(
                    unique_chain[chain1]), str(unique_chain[chain1]), str(unique_chain[chain2]))
                if real_PDB_norm_check(normal_point_lst1[-1], COM[chain1], new_int_site[i][0]) == False:
                    break
                else:
                    normal_point_lst1.remove(normal_point_lst1[-1])
                    print(
                        'Wrong input, please try again! (Wrong input format or n colinear with COM-to-site vector)')
            while True:
                normal_point_lst2 = real_PDB_norm_input(normal_point_lst2, str(
                    unique_chain[chain2]), str(unique_chain[chain1]), str(unique_chain[chain2]))
                if real_PDB_norm_check(normal_point_lst2[-1], COM[chain2], new_int_site[i][1]) == False:
                    break
                else:
                    normal_point_lst2.remove(normal_point_lst2[-1])
                    print(
                        'Wrong input, please try again! (Wrong input format or n colinear with COM-to-site vector)')
            inner_angle = real_PDB_angles(COM[chain1], COM[chain2], new_int_site[i][0], new_int_site[i][1], np.array(
                COM[chain1]) + np.array(normal_point_lst1[-1]), np.array(COM[chain2]) + np.array(normal_point_lst2[-1]))
            angle.append([inner_angle[0], inner_angle[1], inner_angle[2],
                          inner_angle[3], inner_angle[4], inner_angle[5]])
            print("Angles for chain " +
                  str(unique_chain[chain1]) + " & " + str(unique_chain[chain2]))
            print("Theta1: %.3f, Theta2: %.3f, Phi1: %.3f, Phi2: %.3f, Omega: %.3f" % (
                inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4]))

    # generate norm
    if answer_norm == 'yes':
        for i in range(len(reaction_chain)):
            chain1 = 0
            chain2 = 0
            for j in range(len(unique_chain)):
                if reaction_chain[i][0] == unique_chain[j]:
                    chain1 = j
                if reaction_chain[i][1] == unique_chain[j]:
                    chain2 = j
                if reaction_chain[i][0] == unique_chain[chain1] and reaction_chain[i][1] == unique_chain[chain2]:
                    break
            while True:
                normal_point_lst1.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst1[-1], COM[chain1], new_int_site[i][0]) == False:
                    break
                else:
                    normal_point_lst1.remove(normal_point_lst1[-1])
                    normal_point_lst1.append([0., 1., 0.])

            while True:
                normal_point_lst2.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst2[-1], COM[chain2], new_int_site[i][1]) == False:
                    break
                else:
                    normal_point_lst2.remove(normal_point_lst2[-1])
                    normal_point_lst2.append([0., 1., 0.])

            inner_angle = real_PDB_angles(COM[chain1], COM[chain2], new_int_site[i][0], new_int_site[i][1], np.array(
                COM[chain1]) + np.array(normal_point_lst1[-1]), np.array(COM[chain2]) + np.array(normal_point_lst2[-1]))
            angle.append([inner_angle[0], inner_angle[1], inner_angle[2],
                          inner_angle[3], inner_angle[4], inner_angle[5]])
            print("Angles for chain " +
                  str(unique_chain[chain1]) + " & " + str(unique_chain[chain2]))
            print("Theta1: %.3f, Theta2: %.3f, Phi1: %.3f, Phi2: %.3f, Omega: %.3f" % (
                inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4]))

    # looking for chains possess only 1 inferface.
    reaction_chain_1d = []
    one_site_chain = []
    for i in reaction_chain:
        for j in i:
            reaction_chain_1d.append(j)
    for i in unique_chain:
        if reaction_chain_1d.count(i) == 1:
            one_site_chain.append(i)

    # asking whether to center the COM of every chain to origin.
    while True:
        answer2 = input(
            "Do you want each chain to be centered at center of mass? (Type 'yes' or 'no'): ")
        if answer2 == "yes":
            for i in range(len(unique_chain)):
                for k in range(len(reaction_chain)):
                    for j in range(2):
                        if unique_chain[i] == reaction_chain[k][j]:
                            for l in range(3):
                                new_int_site[k][j][l] = new_int_site[k][j][l] - COM[i][l]
                                # angle[k][j+6][l] = angle[k][j+6][l] - COM[i][l]
                for m in range(3):
                    COM[i][m] = 0.0
            break
        if answer2 == "no":
            break
        else:
            print("Invalid answer, please try again.")

    # writing parameters into a file

    f = open("parm.inp", "w")
    f.write(" # Input file\n\n")
    f.write("start parameters\n")
    f.write("    nItr = 1000000\n")
    f.write("    timestep = 0.1\n\n\n")
    f.write("    timeWrite = 500\n")
    f.write("    trajWrite = 500\n")
    f.write("    pdbWrite = 500\n")
    f.write("    restartWrite = 50000\n")
    f.write("    fromRestart = false\n")
    f.write("end parameters\n\n")
    f.write("start boundaries\n")
    f.write("    WaterBox = [494,494,494] #nm\n")
    f.write("    implicitLipid = false\n")
    f.write("    xBCtype = reflect\n")
    f.write("    yBCtype = reflect\n")
    f.write("    zBCtype = reflect\n")
    f.write("end boundaries\n\n")
    f.write("start molecules\n")
    for i in range(len(unique_chain)):
        f.write("     %s:100\n" % (unique_chain[i]))
    f.write("end molecules\n\n")
    f.write("start reactions\n")
    for i in range(len(reaction_chain)):
        molecule1_lower = reaction_chain[i][0].lower()
        molecule2_lower = reaction_chain[i][1].lower()
        f.write("    #### %s - %s ####\n" %
                (reaction_chain[i][0], reaction_chain[i][1]))
        f.write("    %s(%s) + %s(%s) <-> %s(%s!1).%s(%s!1)\n" % (reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower,
                                                                 reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower))
        f.write("    onRate3Dka = 10\n")
        f.write("    offRatekb = 1\n")
        f.write("    sigma = %f\n" % angle[i][5])
        f.write("    norm1 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst1[i][0], normal_point_lst1[i][1], normal_point_lst1[i][2]))
        f.write("    norm2 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst2[i][0], normal_point_lst2[i][1], normal_point_lst2[i][2]))
        if reaction_chain[i][0] in one_site_chain:
            angle[i][2] = 'nan'
        if reaction_chain[i][1] in one_site_chain:
            angle[i][3] = 'nan'
        f.write("    assocAngles = [" + str(angle[i][0]) + "," + str(angle[i][1]) + "," + str(
            angle[i][2]) + "," + str(angle[i][3]) + "," + str(angle[i][4]) + "\n\n")
    f.write("end reactions")
    f.close()

    for i in range(len(unique_chain)):
        mol_file = str(unique_chain[i]) + '.mol'
        f = open(mol_file, "w")
        f.write("##\n# %s molecule information file\n##\n\n" % unique_chain[i])
        f.write("Name    = %s\n" % unique_chain[i])
        f.write("checkOverlap = true\n\n")
        f.write("# translational diffusion constants\n")
        f.write("D       = [12.0,12.0,12.0]\n\n")
        f.write("# rotational diffusion constants\n")
        f.write("Dr      = [0.5,0.5,0.5]\n\n")
        f.write("# Coordinates, with states below, or\n")
        f.write("COM     %.4f    %.4f    %.4f\n" %
                (COM[i][0], COM[i][1], COM[i][2]))
        reaction_chain_merged = []
        chain_string = []
        bond_counter = 0
        for a in range(len(reaction_chain)):
            for b in range(2):
                reaction_chain_merged.append(reaction_chain[a][b])
        if unique_chain[i] not in reaction_chain_merged:
            break
        if unique_chain[i] in reaction_chain_merged:
            bond_counter = 0
            for m in range(len(reaction_chain)):
                if unique_chain[i] == reaction_chain[m][0]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][1])
                    chain_string.append(chain_name.lower())
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][0][0], new_int_site[m][0][1], new_int_site[m][0][2]))
                elif unique_chain[i] == reaction_chain[m][1]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][0])
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][1][0], new_int_site[m][1][1], new_int_site[m][1][2]))
                    chain_string.append(chain_name)
        f.write("\nbonds = %d\n" % bond_counter)
        for j in range(bond_counter):
            f.write("COM %s\n" % chain_string[j])
    return 0

# --------------------------------------Seperated functions (same as above)----------------------------------------

def real_PDB_separate_read(FileName:str):
    total_atom_count = []
    # specific chain the atom belongs to (such as A or B or C, etc).
    total_chain = []
    total_resi_count = []  # residue number
    total_position = []  # the coordinate of each atom
    total_atom_type = []  # to show whether the atom is a alpha carbon, N, etc.
    total_resi_type = []  # to show the type of residue
    # indicate the position of alpha carbon of the residue the atom is in.
    total_resi_position_every_atom = []
    total_resi_position = []  # list of position of all alpha carbon atom position
    total_alphaC_resi_count = []  # indicate which residue the alphaC belongs to
    # The length of last two lists are the same as total residue numbers in the chain and the length of rest of the lists
    # are the same as total atom numbers in the protein.
    # read in user pdb file
    # out data into corresponding lists
    with open(FileName, "r") as filename:
        for line in filename:
            data = line.split()  # split a line into list
            id = data[0]
            if id == 'ENDMDL':
                break
            if id == 'ATOM':  # find all 'atom' lines
                if real_PDB_data_check(data) == 1:
                    pass
                elif real_PDB_data_check(data) == -2:
                    data[3] = data[3].lstrip(data[3][0])
                elif real_PDB_data_check(data) == -1:
                    amino_name = data[2][-3:]
                    data.insert(3, amino_name)
                    data[2] = data[2].rstrip(amino_name)

                total_atom_count.append(data[1])
                total_chain.append(data[4])
                total_resi_count.append(data[5])
                total_atom_type.append(data[2])
                total_resi_type.append(data[3])
                # change all strings into floats for position values, also converting to nm from angstroms
                position_coords = []
                for i in range(3):
                    position_coords.append(float(data[6+i])/10)
                total_position.append(position_coords)
                if data[2] == "CA":
                    total_resi_position.append(position_coords)
                    total_alphaC_resi_count.append(data[5])
    print('Finish reading pdb file')

    # create total_resi_position_every_atom list
    count = 0
    for i in range(len(total_alphaC_resi_count)):
        if count >= len(total_atom_type):
            break
        for j in range(count, len(total_atom_type)):
            if total_resi_count[j] == total_alphaC_resi_count[i]:
                total_resi_position_every_atom.append(total_resi_position[i])
                count = count + 1
            else:
                break

    # determine how many unique chains exist
    unique_chain = []
    for letter in total_chain:
        if letter not in unique_chain:
            unique_chain.append(letter)
    print(str(len(unique_chain)) + ' chain(s) in total: ' + str(unique_chain))

    # exit if there's only one chain.
    if len(unique_chain) == 1:
        sys.exit()

    # create lists of lists where each sublist contains the data for different chains.
    split_atom_count = []
    split_chain = []
    split_resi_count = []
    split_position = []
    split_atom_type = []
    split_resi_type = []
    chain_end_atom = []
    split_resi_position_every_atom = []

    # inner lists are sublists of each list, each of the sublist represents data about a list
    inner_atom_count = []
    inner_chain = []
    inner_resi_count = []
    inner_position = []
    inner_atom_type = []
    inner_resi_type = []
    inner_resi_position_every_atom = []

    # determine number of atoms in each chain
    chain_counter = 0

    for i in range(len(total_atom_count)):

        if total_chain[i] != unique_chain[chain_counter]:
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(inner_resi_position_every_atom)
            inner_atom_count = []
            inner_chain = []
            inner_resi_count = []
            inner_position = []
            inner_atom_type = []
            inner_resi_type = []
            inner_resi_position_every_atom = []
            chain_end_atom.append(len(split_atom_count[chain_counter]))
            chain_counter = chain_counter + 1

        if total_chain[i] == unique_chain[chain_counter]:
            inner_atom_count.append(total_atom_count[i])
            inner_chain.append(total_chain[i])
            inner_resi_count.append(total_resi_count[i])
            inner_position.append(total_position[i])
            inner_atom_type.append(total_atom_type[i])
            inner_resi_type.append(total_resi_type[i])
            inner_resi_position_every_atom.append(
                total_resi_position_every_atom[i])

        if i == (len(total_atom_count) - 1):
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(inner_resi_position_every_atom)
            chain_end_atom.append(len(split_atom_count[chain_counter]))

    print('Each of them has ' + str(chain_end_atom) + ' atoms.')

    # determine the interaction between each two chains by using function chain_int()
    # the output is a tuple with 7 list of list including: reaction_chain, reaction_atom, reaction_atom_position,
    # reaction_atom_distance, reaction_resi_count, reaction_resi_type and  reaction_atom_type

    interaction = real_PDB_chain_int(unique_chain, split_position, split_resi_count, split_atom_count,
                            split_resi_type, split_atom_type, split_resi_position_every_atom)
    reaction_chain = interaction[0]
    reaction_atom = interaction[1]
    reaction_atom_position = interaction[2]
    reaction_atom_distance = interaction[3]
    reaction_resi_count = interaction[4]
    reaction_resi_type = interaction[5]
    reaction_atom_type = interaction[6]
    reaction_resi_position = interaction[7]

    # calculating center of mass (COM) and interaction site

    # COM
    COM = []
    for i in range(len(split_position)):
        sumx = 0
        sumy = 0
        sumz = 0
        for j in range(len(split_position[i])):
            sumx = sumx + split_position[i][j][0]
            sumy = sumy + split_position[i][j][1]
            sumz = sumz + split_position[i][j][2]
        inner_COM = [sumx / len(split_position[i]), sumy /
                    len(split_position[i]), sumz / len(split_position[i])]
        COM.append(inner_COM)

    for i in range(len(COM)):
        print("Center of mass of  " + unique_chain[i] + " is: " +
            "[%.3f, %.3f, %.3f]" % (COM[i][0], COM[i][1], COM[i][2]))


    # int_site
    int_site = []
    two_chain_int_site = []

    for i in range(len(reaction_resi_position)):
        for j in range(0, 2):
            sumx = 0
            sumy = 0
            sumz = 0
            count = 0
            added_position = []
            for k in range(len(reaction_resi_position[i])):
                if reaction_resi_position[i][k][j] not in added_position:
                    sumx = sumx + reaction_resi_position[i][k][j][0]
                    sumy = sumy + reaction_resi_position[i][k][j][1]
                    sumz = sumz + reaction_resi_position[i][k][j][2]
                    added_position.append(reaction_resi_position[i][k][j])
                    count = count + 1
            inner_int_site = [sumx / count, sumy / count, sumz / count]
            two_chain_int_site.append(inner_int_site)
        int_site.append(two_chain_int_site)
        two_chain_int_site = []


    # calculate distance between interaction site.
    int_site_distance = []
    for i in range(len(int_site)):
        distance = math.sqrt((int_site[i][0][0] - int_site[i][1][0]) ** 2 + (int_site[i][0][1] - int_site[i][1][1]) ** 2
                            + (int_site[i][0][2] - int_site[i][1][2]) ** 2)
        int_site_distance.append(distance)

    for i in range(len(int_site)):
        print("Interaction site of " + reaction_chain[i][0] + " & " + reaction_chain[i][1] + " is: "
            + "[%.3f, %.3f, %.3f]" % (int_site[i][0][0],
                                        int_site[i][0][1], int_site[i][0][2]) + " and "
            + "[%.3f, %.3f, %.3f]" % (int_site[i][1][0],
                                        int_site[i][1][1], int_site[i][1][2])
            + " distance between interaction sites is: %.3f nm" % (int_site_distance[i]))

    return reaction_chain, int_site, int_site_distance, unique_chain, COM

def real_PDB_separate_sigma(Result:tuple, ChangeSigma:bool = False, SiteList:list = [], NewSigma:list = []):

    reaction_chain, int_site, int_site_distance, unique_chain, COM = Result
    # user can choose to change the interaction site
    new_int_site_distance = copy.deepcopy(int_site_distance)
    new_int_site = copy.deepcopy(int_site)
    if ChangeSigma:
        for i in range(len(SiteList)):
            n = SiteList[i] - 1
            new_distance = NewSigma[i]
            if new_distance >= 0:
                if n == -1:
                    for p in range(0, len(reaction_chain)):
                        new_int_site_distance[p] = copy.deepcopy(
                            new_distance)
                        dir_vec1 = (
                            int_site[p][0][0] -
                            int_site[p][1][0], int_site[p][0][1] -
                            int_site[p][1][1],
                            int_site[p][0][2] - int_site[p][1][2])
                        dir_vec2 = (
                            int_site[p][1][0] -
                            int_site[p][0][0], int_site[p][1][1] -
                            int_site[p][0][1],
                            int_site[p][1][2] - int_site[p][0][2])
                        unit_dir_vec1 = [dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1),
                                        dir_vec1[2] / real_PDB_mag(dir_vec1)]
                        unit_dir_vec2 = [dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2),
                                        dir_vec2[2] / real_PDB_mag(dir_vec2)]

                        inner_new_position = []
                        new_coord1 = []
                        new_coord2 = []
                        for i in range(3):
                            new_coord1.append(
                                (new_distance - int_site_distance[p]) / 2 * unit_dir_vec1[i] + int_site[p][0][
                                    i])
                            new_coord2.append(
                                (new_distance - int_site_distance[p]) / 2 * unit_dir_vec2[i] + int_site[p][1][
                                    i])
                        inner_new_position.append(new_coord1)
                        inner_new_position.append(new_coord2)

                        new_int_site[p] = copy.deepcopy(
                            inner_new_position)
                        new_int_site_distance[p] = math.sqrt(
                            (new_int_site[p][0][0] -
                            new_int_site[p][1][0]) ** 2
                            + (new_int_site[p][0][1] -
                            new_int_site[p][1][1]) ** 2
                            + (new_int_site[p][0][2] - new_int_site[p][1][2]) ** 2)
                        # print("New interaction site of " + reaction_chain[p][0] + " & " + reaction_chain[p][
                        #     1] + " is: "
                        #     + "[%.3f, %.3f, %.3f]" % (
                        #     new_int_site[p][0][0], new_int_site[p][0][1], new_int_site[p][0][2]) + " and "
                        #     + "[%.3f, %.3f, %.3f]" % (
                        #     new_int_site[p][1][0], new_int_site[p][1][1], new_int_site[p][1][2])
                        #     + " distance between interaction sites is: %.3f" % (new_int_site_distance[p]))
                if n >= 0:
                    new_int_site_distance[n] = copy.deepcopy(
                        new_distance)
                    dir_vec1 = (int_site[n][0][0] - int_site[n][1][0], int_site[n][0]
                                [1] - int_site[n][1][1], int_site[n][0][2] - int_site[n][1][2])
                    dir_vec2 = (int_site[n][1][0] - int_site[n][0][0], int_site[n][1]
                                [1] - int_site[n][0][1], int_site[n][1][2] - int_site[n][0][2])
                    unit_dir_vec1 = [
                        dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1), dir_vec1[2] / real_PDB_mag(dir_vec1)]
                    unit_dir_vec2 = [
                        dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2), dir_vec2[2] / real_PDB_mag(dir_vec2)]

                    inner_new_position = []
                    new_coord1 = []
                    new_coord2 = []
                    for i in range(3):
                        new_coord1.append(
                            (new_distance - int_site_distance[n]) / 2 * unit_dir_vec1[i] + int_site[n][0][i])
                        new_coord2.append(
                            (new_distance - int_site_distance[n]) / 2 * unit_dir_vec2[i] + int_site[n][1][i])
                    inner_new_position.append(new_coord1)
                    inner_new_position.append(new_coord2)

                    new_int_site[n] = copy.deepcopy(inner_new_position)
                    new_int_site_distance[n] = math.sqrt((new_int_site[n][0][0] - new_int_site[n][1][0]) ** 2
                                                        + (new_int_site[n][0][1] - new_int_site[n][1][1]) ** 2
                                                        + (new_int_site[n][0][2] - new_int_site[n][1][2]) ** 2)
                    # print("New interaction site of " + reaction_chain[n][0] + " & " + reaction_chain[n][1] + " is: "
                    #     + "[%.3f, %.3f, %.3f]" % (
                    #         new_int_site[n][0][0], new_int_site[n][0][1], new_int_site[n][0][2]) + " and "
                    #     + "[%.3f, %.3f, %.3f]" % (
                    #     new_int_site[n][1][0], new_int_site[n][1][1], new_int_site[n][1][2])
                    #     + " distance between interaction sites is: %.3f" % (new_int_site_distance[n]) + ' nm')
        
        for i in range(len(new_int_site)):
            print("New interaction site of " + reaction_chain[i][0] + " & " + reaction_chain[i][1] + " is: "
                + "[%.3f, %.3f, %.3f]" % (new_int_site[i][0][0],
                                            new_int_site[i][0][1], new_int_site[i][0][2]) + " and "
                + "[%.3f, %.3f, %.3f]" % (new_int_site[i][1][0],
                                            new_int_site[i][1][1], new_int_site[i][1][2])
                + " distance between new interaction sites is: %.3f nm" % (new_int_site_distance[i]))

        return reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM
        
    else:
        return Result

def real_PDB_separate_angle(Result: tuple):
    reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM = Result
    angle = []
    normal_point_lst1 = []
    normal_point_lst2 = []
    for i in range(len(reaction_chain)):
            chain1 = 0
            chain2 = 0
            for j in range(len(unique_chain)):
                if reaction_chain[i][0] == unique_chain[j]:
                    chain1 = j
                if reaction_chain[i][1] == unique_chain[j]:
                    chain2 = j
                if reaction_chain[i][0] == unique_chain[chain1] and reaction_chain[i][1] == unique_chain[chain2]:
                    break
            while True:
                normal_point_lst1.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst1[-1], COM[chain1], new_int_site[i][0]) == False:
                    break
                else:
                    normal_point_lst1.remove(normal_point_lst1[-1])
                    normal_point_lst1.append([0., 1., 0.])

            while True:
                normal_point_lst2.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst2[-1], COM[chain2], new_int_site[i][1]) == False:
                    break
                else:
                    normal_point_lst2.remove(normal_point_lst2[-1])
                    normal_point_lst2.append([0., 1., 0.])

            inner_angle = real_PDB_angles(COM[chain1], COM[chain2], new_int_site[i][0], new_int_site[i][1], np.array(
                COM[chain1]) + np.array(normal_point_lst1[-1]), np.array(COM[chain2]) + np.array(normal_point_lst2[-1]))
            angle.append([inner_angle[0], inner_angle[1], inner_angle[2],
                        inner_angle[3], inner_angle[4], inner_angle[5]])
            print("Angles for chain " +
                str(unique_chain[chain1]) + " & " + str(unique_chain[chain2]))
            print("Theta1: %.3f, Theta2: %.3f, Phi1: %.3f, Phi2: %.3f, Omega: %.3f" % (
                inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4]))

    # looking for chains possess only 1 inferface.
    reaction_chain_1d = []
    one_site_chain = []
    for i in reaction_chain:
        for j in i:
            reaction_chain_1d.append(j)
    for i in unique_chain:
        if reaction_chain_1d.count(i) == 1:
            one_site_chain.append(i)
    return reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM, angle, normal_point_lst1, normal_point_lst2, one_site_chain

def real_PDB_separate_COM(Result: tuple):
    reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM, angle, normal_point_lst1, normal_point_lst2, one_site_chain = Result
    for i in range(len(unique_chain)):
        for k in range(len(reaction_chain)):
            for j in range(2):
                if unique_chain[i] == reaction_chain[k][j]:
                    for l in range(3):
                        new_int_site[k][j][l] = new_int_site[k][j][l] - COM[i][l]
        for m in range(3):
            COM[i][m] = 0.0
    print('COM is normalized as [0.000, 0.000, 0.000]')
    return reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM, angle, normal_point_lst1, normal_point_lst2, one_site_chain

def real_PDB_separate_write(Result: tuple):
    reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM, angle, normal_point_lst1, normal_point_lst2, one_site_chain = Result
    f = open("parm.inp", "w")
    f.write(" # Input file\n\n")
    f.write("start parameters\n")
    f.write("    nItr = 1000000\n")
    f.write("    timestep = 0.1\n\n\n")
    f.write("    timeWrite = 500\n")
    f.write("    trajWrite = 500\n")
    f.write("    pdbWrite = 500\n")
    f.write("    restartWrite = 50000\n")
    f.write("    fromRestart = false\n")
    f.write("end parameters\n\n")
    f.write("start boundaries\n")
    f.write("    WaterBox = [494,494,494] #nm\n")
    f.write("    implicitLipid = false\n")
    f.write("    xBCtype = reflect\n")
    f.write("    yBCtype = reflect\n")
    f.write("    zBCtype = reflect\n")
    f.write("end boundaries\n\n")
    f.write("start molecules\n")
    for i in range(len(unique_chain)):
        f.write("     %s:100\n" % (unique_chain[i]))
    f.write("end molecules\n\n")
    f.write("start reactions\n")
    for i in range(len(reaction_chain)):
        molecule1_lower = reaction_chain[i][0].lower()
        molecule2_lower = reaction_chain[i][1].lower()
        f.write("    #### %s - %s ####\n" %
                (reaction_chain[i][0], reaction_chain[i][1]))
        f.write("    %s(%s) + %s(%s) <-> %s(%s!1).%s(%s!1)\n" % (reaction_chain[i][0], molecule2_lower,
                                                                reaction_chain[i][1], molecule1_lower,
                                                                reaction_chain[i][0], molecule2_lower,
                                                                reaction_chain[i][1], molecule1_lower))
        f.write("    onRate3Dka = 10\n")
        f.write("    offRatekb = 1\n")
        f.write("    sigma = %f\n" % angle[i][5])
        f.write("    norm1 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst1[i][0], normal_point_lst1[i][1], normal_point_lst1[i][2]))
        f.write("    norm2 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst2[i][0], normal_point_lst2[i][1], normal_point_lst2[i][2]))
        if reaction_chain[i][0] in one_site_chain:
            angle[i][2] = 'nan'
        if reaction_chain[i][1] in one_site_chain:
            angle[i][3] = 'nan'
        f.write("    assocAngles = [" + str(angle[i][0]) + "," + str(angle[i][1]) + "," + str(
            angle[i][2]) + "," + str(angle[i][3]) + "," + str(angle[i][4]) + "\n\n")
    f.write("end reactions")
    f.close()

    for i in range(len(unique_chain)):
        mol_file = str(unique_chain[i]) + '.mol'
        f = open(mol_file, "w")
        f.write("##\n# %s molecule information file\n##\n\n" % unique_chain[i])
        f.write("Name    = %s\n" % unique_chain[i])
        f.write("checkOverlap = true\n\n")
        f.write("# translational diffusion constants\n")
        f.write("D       = [12.0,12.0,12.0]\n\n")
        f.write("# rotational diffusion constants\n")
        f.write("Dr      = [0.5,0.5,0.5]\n\n")
        f.write("# Coordinates, with states below, or\n")
        f.write("COM     %.4f    %.4f    %.4f\n" %
                (COM[i][0], COM[i][1], COM[i][2]))
        reaction_chain_merged = []
        chain_string = []
        bond_counter = 0
        for a in range(len(reaction_chain)):
            for b in range(2):
                reaction_chain_merged.append(reaction_chain[a][b])
        if unique_chain[i] not in reaction_chain_merged:
            break
        if unique_chain[i] in reaction_chain_merged:
            bond_counter = 0
            for m in range(len(reaction_chain)):
                if unique_chain[i] == reaction_chain[m][0]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][1])
                    chain_string.append(chain_name.lower())
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][0][0], new_int_site[m][0][1], new_int_site[m][0][2]))
                elif unique_chain[i] == reaction_chain[m][1]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][0])
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][1][0], new_int_site[m][1][1], new_int_site[m][1][2]))
                    chain_string.append(chain_name)
        f.write("\nbonds = %d\n" % bond_counter)
        for j in range(bond_counter):
            f.write("COM %s\n" % chain_string[j])
    print('Input files written complete.')
    return 0


def real_PDB_show(Result: bool):
    reaction_chain, int_site, int_site_distance, unique_chain, COM = Result
    f = open('show_structure.pdb', 'w')
    f.write('TITLE  PDB\n')
    f.write('REMARK   0 THE COORDINATES IN PDB FILE IS IN UNIT OF ANGSTROM, \n')
    f.write('REMARK   0 SO THE VALUE WILL BE 10 TIMES LARGER THAN NERDSS INPUTS.\n')
    tot_count = 0
    for i in range(len(unique_chain)):
        f.write('ATOM' + ' '*(7-len(str(tot_count))) + str(tot_count) + '  COM' + \
            '   ' + unique_chain[i] + ' '*(5-len(str(i))) + str(i) + \
                ' '*(13-len(str(round(COM[i][0]*10, 3)))) + str(round(COM[i][0]*10, 3)) + \
                    ' '*(8-len(str(round(COM[i][1]*10, 3)))) + str(round(COM[i][1]*10, 3)) + \
                        ' '*(8-len(str(round(COM[i][2]*10, 3)))) + str(round(COM[i][2]*10, 3)) + \
                            '     0     0CL\n')
        tot_count += 1
        for j in range(len(reaction_chain)):
            if unique_chain[i] in reaction_chain[j]:
                if unique_chain[i] == reaction_chain[j][0]:
                    # react_site = reaction_chain[j][1].lower()
                    react_coord = int_site[j][0]
                else:
                    # react_site = reaction_chain[j][0].lower()
                    react_coord = int_site[j][1]
                react_site = reaction_chain[j][0].lower() + reaction_chain[j][1].lower()
                f.write('ATOM' + ' '*(7-len(str(tot_count))) + str(tot_count) + \
                    ' '*(5-len(str(react_site))) + str(react_site) + \
                        '   ' + unique_chain[i] + ' '*(5-len(str(i))) + str(i) + \
                            ' '*(13-len(str(round(react_coord[0]*10, 3)))) + str(round(react_coord[0]*10, 3)) + \
                                ' '*(8-len(str(round(react_coord[1]*10, 3)))) + str(round(react_coord[1]*10, 3)) + \
                                    ' '*(8-len(str(round(react_coord[2]*10, 3)))) + str(round(react_coord[2]*10, 3)) + \
                                        '     0     0CL\n')
                tot_count += 1
    print('PDB writing complete! (named as show_structure.pdb)')
    return 0