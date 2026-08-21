import { useState } from "react";
import { createLostItem } from "../services/api";

function ReportLostItem() {
  const [form, setForm] = useState({
    item_name: "",
    description: "",
    location: "",
    lost_time: "",
    contact: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      await createLostItem({
        ...form,
        lost_time: new Date(form.lost_time).toISOString(),
      });

      setMessage("Lost item reported successfully.");

      setForm({
        item_name: "",
        description: "",
        location: "",
        lost_time: "",
        contact: "",
      });
    } catch (error) {
      console.error(error);
      setMessage("Failed to report lost item.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Report Lost Item</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Item Name</label>
          <input
            name="item_name"
            value={form.item_name}
            onChange={handleChange}
            placeholder="Black Backpack"
            required
          />
        </div>

        <div>
          <label>Description</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Black backpack with laptop compartment"
            required
          />
        </div>

        <div>
          <label>Location</label>
          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="Near Library"
            required
          />
        </div>

        <div>
          <label>Lost Time</label>
          <input
            type="datetime-local"
            name="lost_time"
            value={form.lost_time}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Contact</label>
          <input
            name="contact"
            value={form.contact}
            onChange={handleChange}
            placeholder="+91XXXXXXXXXX"
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Report Lost Item"}
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default ReportLostItem;