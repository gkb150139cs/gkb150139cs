async createBrokersCompany(createBrokersCompany: CreateBrokersDto) {
        logger.trace("Entering createBrokersCompany function.");
        logger.debug(`createBrokersCompany - createBrokersCompany: ${JSON.stringify(createBrokersCompany)}`);
        try {
            logger.info("createBrokersCompany - Checking if broker company already exists.");
            let existingCompany = null;
            if (createBrokersCompany.email) {
                existingCompany = await this.companyRepository.findOne({
                    where: [
                        { email: createBrokersCompany.email }
                    ],
                });
            }  

            if (existingCompany) {
                logger.warn(`createBrokersCompany - Company already exists with email: ${createBrokersCompany.email}`);
                RESPONSES.RESPONSE_NOT_FOUND.data = 'Company already exists.';
                return RESPONSES.RESPONSE_NOT_FOUND;
            }

            logger.info("createBrokersCompany - Creating new broker company entity.");
            let company = new Company();
            company.type = CompanyType.BROKER
            Object.assign(company, createBrokersCompany);
            
            logger.info("createBrokersCompany - Saving broker company to database.");
            await this.companyRepository.save(company);
            logger.info(`createBrokersCompany - Broker company created successfully with ID: ${company.id}`);

            RESPONSES.SUCCESS_RESPONSE.data = "Broker company created successfully."
            return RESPONSES.SUCCESS_RESPONSE;
        } catch (error) {
            logger.error(`Error in createBrokersCompany: ${error.message}`, error);
            throw new Error('An error occurred while creating the company.');
        }
    }
