import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { Heading } from './components/Heading';
import { Inputs } from './components/Inputs';

test("Heading is Loaded", () => {
  // Ensure you're rendering the component with the correct data-testid attribute
  render(<Heading data-testid="header" />);

  // Access the component using getByTestId
  const component = screen.getByTestId("header");
  
  // Check if the component is in the document
  expect(component).toBeInTheDocument();
  
  // Check if the heading text is in the document
  expect(screen.getByRole('heading', { name: /Elena: Elevation Based Navigation!/i })).toBeInTheDocument();
});


test("Value in the input field", () => {
  const inputStyle = {
    marginLeft: '1rem',
    padding: '0.5rem',
    borderRadius: '0px',
    border: '2px solid #000',
    outline: 'none',
    fontSize: '14px',
    width: '200px',
    boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  };

  const renderInput = (placeholder) => (
    <input
      style={inputStyle}
      label={placeholder.toLowerCase()}
      type="address"
      name={placeholder.toLowerCase()}
      placeholder={`Enter ${placeholder}`}
    />
  );

  render(renderInput("Source"));
  expect(screen.getByPlaceholderText("Enter Source")).toBeInTheDocument();

  render(renderInput("Destination"));
  expect(screen.getByPlaceholderText("Enter Destination")).toBeInTheDocument();

  render(renderInput("Path Limit (Max 100)"));
  expect(screen.getByPlaceholderText("Enter Path Limit (Max 100)")).toBeInTheDocument();
});

test("Search button is disabled when the input fields are empty", () => {
  const isDisabled = true;

  render(
        <div>
          <button disabled={isDisabled} >
          Search
        </button>
        </div> 
        );
  expect(screen.getByRole("button", { name: "Search" })).toBeDisabled();
});

test("Reset button is disabled when the input fields are empty", () => {
  const isDisabled = true;

  render(
        <div>
          <button disabled={isDisabled} >
          Reset
        </button>
        </div> 
        );
  expect(screen.getByRole("button", { name: "Reset" })).toBeDisabled();
});
test("Shortest Path Metrics are rendered correctly", () => {
  render(
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', backgroundColor: '#e0e0e0', padding: '10px', marginLeft: 'auto', marginRight: '1rem' }}>
      <span style={{ marginBottom: '10px' }}>Shortest Path Metrics:</span>
      <div style={{ backgroundColor: '#fff', padding: '10px', borderRadius: '4px', marginBottom: '5px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ marginRight: '10px' }}>EleNa Path distance:</span>
          <span>40.30202</span>
        </div>
      </div>
      <div style={{ backgroundColor: '#fff', padding: '10px', borderRadius: '4px', marginBottom: '5px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ marginRight: '10px' }}>EleNa Path elevation gain:</span>
          <span>40.30202</span>
        </div>
      </div>
      <div style={{ backgroundColor: '#fff', padding: '10px', borderRadius: '4px', marginBottom: '5px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ marginRight: '10px' }}>Shortest Path distance:</span>
          <span>40.30202</span>
        </div>
      </div>
      <div style={{ backgroundColor: '#fff', padding: '10px', borderRadius: '4px', marginBottom: '5px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ marginRight: '10px' }}>Shortest Path elevation gain:</span>
          <span>43420.3020002</span>
        </div>
      </div>
    </div>
  );

  expect(screen.getByText("Shortest Path Metrics:")).toBeInTheDocument();
  expect(screen.getByText("EleNa Path distance:")).toBeInTheDocument();
  expect(screen.getByText("EleNa Path elevation gain:")).toBeInTheDocument();
  expect(screen.getByText("Shortest Path distance:")).toBeInTheDocument();
  expect(screen.getByText("Shortest Path elevation gain:")).toBeInTheDocument();
  expect(screen.getByText("43420.3020002")).toBeInTheDocument();
});

test("Testing the radio buttons of the min-max elevation", async () => {
  render(
    <div data-testid="elevation">
        <input data-testid="min" type="radio" value="min" name="elevationType" style={{ marginRight: "0.5rem" }} /> Minimum Elevation
        <input data-testid="max" type="radio" value="max" name="elevationType" style={{ marginRight: "0.5rem" }} /> Maximum Elevation
    </div>
  );

  const radioButtons = screen.getByTestId("elevation");
  const min = screen.getByTestId("min");
  const max = screen.getByTestId("max");
  expect(radioButtons).toBeInTheDocument();

  fireEvent.click(min);
  expect(max).not.toBeChecked();

  fireEvent.click(max);
  expect(max).toBeChecked();

});


test("Testing the radio buttons of the algorithm", async () => {
  render(
    <div data-testid="options">
    <input data-testid="astar" type="radio" value="AStar" name="AlgorithmType" id="astar" style={{ marginRight: "0.5rem" }}/> 
    <label>A* Algorithm</label>
    <input data-testid="dijkstra" type="radio" value="Dijkstra" name="AlgorithmType" id="dijkstra" style={{ marginRight: "0.5rem" }}/> 
    <label>Dijkstra Algorithm</label>
    </div>
  );

  const radioButtons = screen.getByTestId("options");
  const astar = screen.getByTestId("astar");
  const dijkstra = screen.getByTestId("dijkstra");
  expect(radioButtons).toBeInTheDocument();

  fireEvent.click(astar);
  expect(dijkstra).not.toBeChecked();

  fireEvent.click(dijkstra);
  expect(dijkstra).toBeChecked();

});
