from great_expectations.core import ExpectationSuite, ExpectationConfiguration



def build_expectation_suite() -> ExpectationSuite:
    """
    Fungsi ini untuk membangun sebuah
     "expectation suite" atau kumpulan harapan
      validasi terkait data yang diberikan.
    """

    expectation_suite_energy_consumption = ExpectationSuite(
        expectation_suite_name="energy_consumption"
    )

    # Column
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list":[
                    "datetime_utc",
                    "area",
                    "consumer_type",
                    "energy_consumption"
                ]
            }
        )
    )

    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal", kwargs={"value": 4}
        )
    )

    # Datetime UTC
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "datetime_utc"}
        )
    )

    # Area
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={
                "column": "area",
                "value_set": (
                0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                10, 11, 12, 13, 14, 15, 16,17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32, 33
                )
            }
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "area", "type_": "int8"},
        )
    )

    # Consumer type
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={
                "column": "consumer_type",
                "value_set": (
                    0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                    10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
                ),
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "consumer_type", "type_": "int8"},
        )
    )

    # Energy consumption
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "energy_consumption",
                "min_value": 0,
                "strict_min": False,
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "energy_consumption", "type_": "float64"},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "energy_consumption"},
        )
    )

    return expectation_suite_energy_consumption