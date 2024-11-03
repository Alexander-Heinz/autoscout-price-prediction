import React, { useState } from 'react';
import uniqueValues from './unique_values.json'; // Import the JSON file

const CarForm = () => {
  const [formData, setFormData] = useState({
    model: '',
    mileage_in_km: '',
    year: '',
    brand: '',
    transmission_type: '',
    power_ps: '' // Add power_ps to the initial formData state
  });
  const [price, setPrice] = useState(null);
  const [models, setModels] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    // If the brand is changed, update the models and reset the model field
    if (name === 'brand') {
      setModels(uniqueValues.brands_models[value] || []);
      setFormData((prevData) => ({
        ...prevData,
        brand: value,
        model: ''
      }));
    } else {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value
      }));
    }
  };

  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setPrice(data.price);
    } catch (error) {
      console.error('Error making prediction', error);
    }
  };

  return (
    <div>
      <h1>Car Price Estimator</h1>
      <form onSubmit={handleSubmit}>
        <select name="brand" onChange={handleChange} value={formData.brand}>
          <option value="">Select Brand</option>
          {Object.keys(uniqueValues.brands_models).map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
        <select name="model" onChange={handleChange} value={formData.model} disabled={!formData.brand}>
          <option value="">Select Model</option>
          {models.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))}
        </select>
        <select name="transmission_type" onChange={handleChange} value={formData.transmission_type}>
          <option value="">Select Transmission Type</option>
          {uniqueValues.transmission_types.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
        <input
          name="mileage_in_km"
          type="number"
          onChange={handleChange}
          value={formData.mileage_in_km}
          placeholder="Mileage (km)"
        />
        <input
          name="year"
          type="number"
          onChange={handleChange}
          value={formData.year}
          placeholder="Year"
        />
        <input
          name="power_ps"
          type="number"
          onChange={handleChange}
          value={formData.power_ps}
          placeholder="Power (PS)"
        />
        <button type="submit">Get Price</button>
      </form>
      {price !== null && <p>Estimated Price: {price}</p>}
    </div>
  );
};

export default CarForm;
