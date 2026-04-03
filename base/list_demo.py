import dataclasses


@dataclasses.dataclass
class Address:
    input: list[str]
    output: list[str]


if __name__ == "__main__":
    input_data = ["in1", "in2", "in3"]
    output_data = ["out1", "out2", "out3"]
    address = Address(input=input_data, output=output_data)
    print(address.input)
    (in1, in2, in3) = address.input
    print(in1)
