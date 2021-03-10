/* eslint-disable react/react-in-jsx-scope */
import './App.css';
import { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import React from 'react';
import { LineChart, CartesianGrid, Legend, Line, Tooltip, XAxis, YAxis } from 'recharts';
import Table from './Table';
import { SetStateAction } from 'react';

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
function App() {
    const [dats, setDats]: SetStateAction<[]> = useState(null);
    useEffect(() => {
        (async () => {
            const data = await callAPI();
            console.log(data);
            setDats(data['data']);
            console.log(typeof dats);
        })();
    }, []);
    function callAPI() {
        const data = axios
            .get(`http://127.0.0.1:5000/`)
            .then((promise) => {
                return promise.data;
            })
            .catch((e) => {
                console.error(e);
            });
        return data;
    }
    const columns = useMemo(
        () => [
            {
                // first group - TV Show
                Header: 'Stonks',
                // First group columns
                columns: [
                    {
                        Header: 'close',
                        accessor: '["close"]',
                    },
                    {
                        Header: 'high',
                        accessor: 'dats.high',
                    },
                    {
                        Header: 'low',
                        accessor: 'dats.low',
                    },
                    {
                        Header: 'volume',
                        accessor: 'dats.volume',
                    },
                    {
                        Header: 'awesome',
                        accessor: 'dats.awesome',
                    },
                    {
                        Header: 'accel_oss',
                        accessor: 'dats.accel_oss',
                    },
                    {
                        Header: 'accum_dist',
                        accessor: 'dats.accum_dist',
                    },
                ],
            },
        ],
        [],
    );

    return (
        <div className="App">
            <LineChart
                style={{ margin: '100px' }}
                width={1000}
                height={1000}
                data={dats}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} />
                <Line type="monotone" dataKey="sma" stroke="red" dot={false} />
                <Line type="monotone" dataKey="exp_moving_avg" stroke="#0884d8" dot={false} />
            </LineChart>
            <Table columns={columns} data={dats} />
        </div>
    );
}

export default App;
