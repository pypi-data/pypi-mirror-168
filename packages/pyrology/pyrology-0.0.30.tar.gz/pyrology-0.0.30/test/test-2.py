#!/usr/bin/python3

from pyrology import pyrology


def pippo():
    print('PIPPO')

if __name__ == '__main__':
    print('===============================================================')

    ns = pyrology.Simplespace()
    ns.a.b.c = 1234567890
    print(ns.a.b.c)

    print('===============================================================')

    ds = pyrology.Tablespace()
    ds.a.b.c = 3
    print(ds.a.b.c)
    print(ds.get('a.b.c'))
    ds.set('x.y.z', 999)
    print(ds.x.y.z)
    print(ds.get('x.y.z'))
    ds.set('x.y.pippoz', pippo)
    ds.x.y.pippoz()
    ds.x.y.plutoz = pippo
    ds.x.y.plutoz()

    print(ds.table())
    print(ds.table()['x.y.z'])

    for key in ds.table():
        print(key)

    for key, value in ds.table().items():
        print(key, value)

    print(ds.get('x.y.z'))

    print('===============================================================')

    ds = pyrology.Dotspace().walk('/home/pindar/pindar-dev/repository/pyrology/test/schema', ['*.py', '*.txt'])

    print(ds.host1.aaa.zzz.v)
    print(ds.host1.eee.t)

    ds.host1.aaa.zzz.example.pippo()
    ds.host2.eee.example1.pippo10()

    barberis = ds.host2.eee.u.i.o.p.example.Cesare('cesarino')
    barberis.show()

    ds.host2.eee.u.i.o.p.example.Cesare('cesarino').show()

    print('===============================================================')

    ds = pyrology.Dotspace().walk('/home/pindar/pindar-dev/repository/pyrology/test/schema2')
    print(ds.host1.c)
    print(ds.host1.f1.f2.f3.f4.f)
    ds.host2.u.i.o.p.example.Cesare('cesarino').show()

    print('===============================================================')

    xx = pyrology.Dotspace().load('/home/pindar/pindar-dev/repository/pyrology/test/schema2/host2', 'u.i.o.p.example.py')
    xx.u.i.o.p.example.Cesare('cesarino').show()

    xx = pyrology.Dotspace().load('/home/pindar/pindar-dev/repository/pyrology/test/schema2', 'host2/u.i.o.p.example.py')
    xx.host2.u.i.o.p.example.Cesare('cesarino').show()

    print('===============================================================')


