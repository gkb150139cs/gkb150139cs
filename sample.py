def process_file(cfg: JobConfig) -> Path:
    """Read -> validate -> normalize -> write. Retries only on I/O."""
    attempt = 0
    while True:
        try:
            log.info("Reading %s", cfg.input_path)
            df = read_csv(cfg.input_path)

            log.info("Validating schema")
            validate_schema(df, cfg.required_columns)

            log.info("Normalizing %d columns", len(cfg.null_columns))
            df = normalize_columns(df, cfg.null_columns)

            log.info("Writing to sink")
            cfg.sink.write(df)
            return getattr(cfg.sink, "path", Path("."))  # best effort for callers
        except RetryableIOError as e:
            attempt += 1
            if attempt > cfg.max_retries:
                log.exception("I/O failed after %d attempts", attempt)
                raise
            sleep = cfg.backoff_seconds * (2 ** (attempt - 1))
            log.warning("I/O error (%s). Retrying in %.1fs (%d/%d)...", e, sleep, attempt, cfg.max_retries)
            time.sleep(sleep)
        except DataValidationError:
            # Non-retryable by design: surface immediately with context
            log.exception("Validation failed")
            raise
