/**
 * Template: Value Object
 * 
 * Value Objects são imutáveis e comparados por valor, não por identidade.
 * 
 * Regras:
 * - SEMPRE imutável (readonly em todas as props)
 * - Construtor privado (use factory method create())
 * - Valida no momento da criação
 * - Métodos que "modificam" retornam NOVA instância
 * - equals() compara por valor
 */

import { ValueObject } from '@core/domain/base/value-object.base';

// Erros de domínio
// import { Invalid__VO_NAME__Error } from '../errors';

// Props do Value Object
interface __VO_NAME__Props {
  readonly value: string; // Ajuste o tipo conforme necessário
}

export class __VO_NAME__ extends ValueObject<__VO_NAME__Props> {
  // ==========================================
  // Getters
  // ==========================================
  
  get value(): string {
    return this.props.value;
  }
  
  // ==========================================
  // Factory Method
  // ==========================================
  
  /**
   * Cria uma nova instância do Value Object
   * @throws Invalid__VO_NAME__Error se valor inválido
   */
  public static create(value: string): __VO_NAME__ {
    // Validações
    if (!value || value.trim().length === 0) {
      // throw new Invalid__VO_NAME__Error('Value cannot be empty');
      throw new Error('Value cannot be empty');
    }
    
    // Outras validações específicas
    // if (value.length > 100) {
    //   throw new Invalid__VO_NAME__Error('Value too long');
    // }
    
    return new __VO_NAME__({ value: value.trim() });
  }
  
  // ==========================================
  // Métodos de Transformação (retornam NOVA instância)
  // ==========================================
  
  /**
   * Exemplo: método que retorna nova instância
   */
  // public toUpperCase(): __VO_NAME__ {
  //   return __VO_NAME__.create(this.value.toUpperCase());
  // }
  
  // ==========================================
  // Métodos Utilitários
  // ==========================================
  
  /**
   * Retorna representação em string
   */
  public toString(): string {
    return this.value;
  }
  
  // ==========================================
  // Construtor Privado
  // ==========================================
  
  private constructor(props: __VO_NAME__Props) {
    super(props);
  }
}

// ============================================
// Exemplo de Value Object Composto (ex: Money)
// ============================================

/*
interface MoneyProps {
  readonly amount: number;
  readonly currency: Currency;
}

export class Money extends ValueObject<MoneyProps> {
  get amount(): number {
    return this.props.amount;
  }
  
  get currency(): Currency {
    return this.props.currency;
  }
  
  public static create(amount: number, currency: Currency): Money {
    if (amount < 0) {
      throw new InvalidMoneyError('Amount cannot be negative');
    }
    return new Money({ amount, currency });
  }
  
  public add(other: Money): Money {
    if (!this.currency.equals(other.currency)) {
      throw new CurrencyMismatchError();
    }
    return Money.create(this.amount + other.amount, this.currency);
  }
  
  public multiply(factor: number): Money {
    return Money.create(this.amount * factor, this.currency);
  }
  
  private constructor(props: MoneyProps) {
    super(props);
  }
}
*/
