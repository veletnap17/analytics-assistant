import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from "recharts";

function isDateLike(value) {
  if (typeof value !== "string") return false;

  return (
    /^\d{4}-\d{2}(-\d{2})?/.test(value) ||
    /^\d{2}[./]\d{2}[./]\d{4}/.test(value)
  );
}

function formatNumber(value) {
  if (typeof value !== "number") return value;

  return Math.round(value).toLocaleString();
}

function formatCategory(value, column) {
  if (
    typeof value !== "string" ||
    !/^\d{4}-\d{2}-\d{2}T/.test(value)
  ) {
    return value;
  }

  const [year, month, day] = value.slice(0, 10).split("-");

  if (column.toLowerCase().includes("month")) {
    return new Date(+year, +month - 1).toLocaleDateString("en-GB", {
      month: "short",
      year: "numeric"
    });
  }

  return `${day}/${month}/${year}`;
}

export default function ResultChart({ data }) {
  if (!data?.length || data.length < 2) return null;

  const columns = Object.keys(data[0]);

  const numeric = columns.find(
    column => typeof data[0][column] === "number"
  );

  const category = columns.find(
    column => column !== numeric
  );

  if (!numeric || !category) return null;

  const chartData = data.slice(0, 20);
  const temporal = isDateLike(chartData[0][category]);

  const title =
    `${numeric.replaceAll("_", " ")} by ${category.replaceAll("_", " ")}`;

  return (
    <div className="resultChart">
      <h3>{title}</h3>

      <ResponsiveContainer width="100%" height={300}>
        {temporal ? (
          <LineChart data={chartData}>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey={category}
              tickFormatter={value =>
                formatCategory(value, category)
              }
            />

            <YAxis
              tickFormatter={formatNumber}
            />

            <Tooltip
              formatter={formatNumber}
              labelFormatter={value =>
                formatCategory(value, category)
              }
            />

            <Line
              type="monotone"
              dataKey={numeric}
              stroke="#19d9cc"
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        ) : (
          <BarChart data={chartData}>
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
            />

            <XAxis
              dataKey={category}
              tickFormatter={value =>
                formatCategory(value, category)
              }
              interval={0}
              angle={-20}
              textAnchor="end"
              height={80}
            />

            <YAxis
              tickFormatter={formatNumber}
            />

            <Tooltip
              formatter={formatNumber}
              labelFormatter={value =>
                formatCategory(value, category)
              }
            />

            <Bar
              dataKey={numeric}
              fill="#19d9cc"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}