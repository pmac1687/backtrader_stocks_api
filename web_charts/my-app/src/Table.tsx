/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable react/jsx-key */
/* eslint-disable react/react-in-jsx-scope */
import { useTable } from 'react-table';

type TableProps = {
    data: [
        {
            close: number;
            open: number;
            high: number;
            low: number;
            volume: number;
            awesome: number;
            accel_oss: number;
            accum_dist: number;
        },
    ];
    columns: { Header: string; columns: { Header: string; accessor: string }[] }[];
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default function Table({ columns, data }: TableProps) {
    const {
        getTableProps, // table props from react-table
        getTableBodyProps, // table body props from react-table
        headerGroups, // headerGroups, if your table has groupings
        rows, // rows for the table based on the data passed
        prepareRow, // Prepare the row (this function needs to be called for each row before getting the row props)
    } = useTable({
        columns,
        data,
    });
    return (
        <table {...getTableProps()}>
            <thead>
                {headerGroups.map((headerGroup) => (
                    <tr {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map((column) => (
                            <th {...column.getHeaderProps()}>{column.render('Header')}</th>
                        ))}
                    </tr>
                ))}
            </thead>
            <tbody {...getTableBodyProps()}>
                {rows.map((row, _i) => {
                    prepareRow(row);
                    return (
                        <tr {...row.getRowProps()}>
                            {row.cells.map((cell) => {
                                return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>;
                            })}
                        </tr>
                    );
                })}
            </tbody>
        </table>
    );
}
