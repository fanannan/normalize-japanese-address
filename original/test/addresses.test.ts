import {normalize} from '../src/main'

import fs from 'fs'
import path from 'path'

const lines = fs
    .readFileSync(path.join(path.dirname(__filename), '/addresses.csv'), {
        encoding: 'utf-8',
    })
    .split(/\n/)
lines.shift() // 見出し行

lines.forEach((line) => {
    if (line) {
        const data = line.trim().split(/,/)

        test(data[0], async () => {
            const res = await normalize(data[0])
            expect(res.pref).toStrictEqual(data[1])
            expect(res.city).toStrictEqual(data[2])
            expect(res.town).toStrictEqual(data[3])
            expect(res.addr).toStrictEqual(data[4])
        })
    }
})
