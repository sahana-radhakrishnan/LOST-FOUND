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
      console.error("Failed to report lost item:", error);
      setMessage(
        "Backend is currently unavailable. Your form is ready to submit once the API is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page-header">
        <h1>Report Lost Item</h1>
        <p>
          Provide detailed information to start an investigation.
        </p>
      </div>

      <div className="card form-card">
        <div className="section-heading">
          <div className="section-icon">+</div>

          <div>
            <h2 className="card-title">Lost Item Information</h2>
            <p className="card-subtitle">
              The investigation agent will use these details to
              search for possible matches.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="item_name">Item Name</label>

              <input
                id="item_name"
                name="item_name"
                value={form.item_name}
                onChange={handleChange}
                placeholder="e.g. Black Backpack"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="contact">Contact</label>

              <input
                id="contact"
                name="contact"
                value={form.contact}
                onChange={handleChange}
                placeholder="+91XXXXXXXXXX"
                required
              />
            </div>

            <div className="form-group full">
              <label htmlFor="description">Description</label>

              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe color, size, brand, identifying marks, contents, etc."
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="location">Last Known Location</label>

              <input
                id="location"
                name="location"
                value={form.location}
                onChange={handleChange}
                placeholder="e.g. Near Library"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="lost_time">Lost Time</label>

              <input
                id="lost_time"
                type="datetime-local"
                name="lost_time"
                value={form.lost_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-actions">
            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Submitting..." : "Start Investigation"}
            </button>
          </div>

          {message && (
            <div className="message">
              {message}
            </div>
          )}
        </form>
      </div>

      <div className="info-banner">
        <div className="info-banner-icon">i</div>

        <div>
          <strong>What happens next?</strong>

          <p>
            The investigation agent will search reported lost
            items and detected objects, compare their attributes,
            and identify possible matches.
          </p>
        </div>
      </div>
    </>
  );
}

export default ReportLostItem;