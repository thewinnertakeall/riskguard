export default function RF07Section({
  title,
  description,
  children,
}) {
  return (
    <section className="rf07-section">
      <header className="rf07-section-header">
        <div>
          <h3>{title}</h3>

          {description && (
            <p>{description}</p>
          )}
        </div>
      </header>

      {children}
    </section>
  );
}
